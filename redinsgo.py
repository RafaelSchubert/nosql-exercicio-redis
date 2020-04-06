import random
import redis


REDIS_CONEXAO_HOST = 'localhost'
REDIS_CONEXAO_PORT = 6379

# Significa [1, 100), ou o mesmo que [1, 99].
BINGO_NUMEROS_INTERVALO = (1, 100)
BINGO_JOGADORES_QUANTIDADE = 50
BINGO_CARTELA_NUMEROS_QUANTIDADE = 15

CHAVE_BINGO_NUMEROS = 'bingo:numeros'
CHAVE_JOGADOR_PREFIXO = 'usuario'
CHAVE_JOGADOR_NOME = 'nome'
CHAVE_JOGADOR_CARTELA = 'bcartela'
CHAVE_CARTELA_PREFIXO = 'cartela'

JOGADOR_NOMES = ['João', 'Paulo', 'Pedro', 'Bernardo', 'André', 'Eduardo', 'Gilberto', 'Lucas', 'Afonso']
JOGADOR_SOBRENOMES = ['Silva', 'Torres', 'Pereira', 'Silveira', 'Brasil', 'Felipe', 'Nobre', 'Carvalho']


conexao_redis = None


def montar_chave_jogador(numero):
    return f'{CHAVE_JOGADOR_PREFIXO}:{numero}'


def montar_chave_cartela(numero):
    return f'{CHAVE_CARTELA_PREFIXO}:{numero}'


def gerar_nome_jogador():
    return f'{random.choice(JOGADOR_NOMES)} {random.choice(JOGADOR_SOBRENOMES)}'


def intervalo_numeros_jogadores():
    return range(1, 1 + BINGO_JOGADORES_QUANTIDADE)


def limpar_database():
    global conexao_redis

    conexao_redis.flushdb()


def carregar_numeros_bingo():
    global conexao_redis

    print(f'O jogo usará pedras numeradas de {BINGO_NUMEROS_INTERVALO[0]} a {BINGO_NUMEROS_INTERVALO[1] - 1}.')

    conexao_redis.sadd(CHAVE_BINGO_NUMEROS, *range(*BINGO_NUMEROS_INTERVALO))


def carregar_jogadores_bingo():
    global conexao_redis

    print('Carregar perfis dos jogadores:')
    print()

    for numero in intervalo_numeros_jogadores():
        chave_jogador = montar_chave_jogador(numero)
        nome_jogador = gerar_nome_jogador()

        print(f'{chave_jogador}: {CHAVE_JOGADOR_NOME}={nome_jogador}')

        conexao_redis.hset(chave_jogador, CHAVE_JOGADOR_NOME, nome_jogador)

    print()


def carregar_cartelas_bingo():
    global conexao_redis

    print('Carregar as cartelas dos jogadores:')
    print()

    for numero in intervalo_numeros_jogadores():
        chave_jogador = montar_chave_jogador(numero)
        chave_cartela = montar_chave_cartela(numero)

        numeros_cartela = set()

        while len(numeros_cartela) < BINGO_CARTELA_NUMEROS_QUANTIDADE:
            numeros_cartela.add(int(conexao_redis.srandmember(CHAVE_BINGO_NUMEROS)))

        print(f'{chave_jogador} --> {chave_cartela}: {sorted(numeros_cartela)}')

        conexao_redis.sadd(chave_cartela, *numeros_cartela)
        conexao_redis.hset(chave_jogador, CHAVE_JOGADOR_CARTELA, chave_cartela)


def main():
    global conexao_redis

    print('REDINSGO: Bingo com Redis')
    print()

    with redis.Redis(REDIS_CONEXAO_HOST, REDIS_CONEXAO_PORT) as conexao_redis:
        limpar_database()

        carregar_numeros_bingo()
        carregar_jogadores_bingo()
        carregar_cartelas_bingo()


if __name__ == '__main__':
    main()