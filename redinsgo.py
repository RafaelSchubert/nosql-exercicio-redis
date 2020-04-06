import random
import redis


REDIS_CONEXAO_HOST = 'localhost'
REDIS_CONEXAO_PORT = 6379

# Significa [1, 100), ou o mesmo que [1, 99].
BINGO_NUMEROS_INTERVALO = (1, 100)
BINGO_JOGADORES_QUANTIDADE = 50

CHAVE_BINGO_NUMEROS = 'bingo:numeros'
CHAVE_JOGADOR_PREFIXO = 'usuario'
CHAVE_JOGADOR_NOME = 'nome'

JOGADOR_NOMES = ['João', 'Paulo', 'Pedro', 'Bernardo', 'André', 'Eduardo', 'Gilberto', 'Lucas', 'Afonso']
JOGADOR_SOBRENOMES = ['Silva', 'Torres', 'Pereira', 'Silveira', 'Brasil', 'Felipe', 'Nobre', 'Carvalho']


conexao_redis = None


def limpar_database():
    global conexao_redis

    conexao_redis.flushdb()


def carregar_numeros_bingo():
    global conexao_redis

    print(f'O jogo usará pedras numeradas de {BINGO_NUMEROS_INTERVALO[0]} a {BINGO_NUMEROS_INTERVALO[1] - 1}.')

    conexao_redis.sadd(CHAVE_BINGO_NUMEROS, *range(*BINGO_NUMEROS_INTERVALO))


def gerar_nome_jogador():
    return f'{random.choice(JOGADOR_NOMES)} {random.choice(JOGADOR_SOBRENOMES)}'


def montar_chave_jogador(numero):
    return f'{CHAVE_JOGADOR_PREFIXO}:{numero}'


def carregar_jogadores_bingo():
    global conexao_redis

    print('Carregar perfis dos jogadores:')
    print()

    for numero in range(1, 1 + BINGO_JOGADORES_QUANTIDADE):
        chave_jogador = montar_chave_jogador(numero)
        nome_jogador = gerar_nome_jogador()

        print(f'{chave_jogador}: {CHAVE_JOGADOR_NOME}={nome_jogador}')

        conexao_redis.hset(chave_jogador, CHAVE_JOGADOR_NOME, nome_jogador)

    print()


def main():
    global conexao_redis

    print('REDINSGO: Bingo com Redis')
    print()

    with redis.Redis(REDIS_CONEXAO_HOST, REDIS_CONEXAO_PORT) as conexao_redis:
        limpar_database()

        carregar_numeros_bingo()
        carregar_jogadores_bingo()

if __name__ == '__main__':
    main()