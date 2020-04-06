import redis


REDIS_CONEXAO_HOST = 'localhost'
REDIS_CONEXAO_PORT = 6379


# Significa [1, 100), ou o mesmo que [1, 99].
BINGO_NUMEROS_INTERVALO = (1, 100)


CHAVE_BINGO_NUMEROS = 'bingo:numeros'


conexao_redis = None


def carregar_numeros_bingo():
    global conexao_redis

    print(f'O jogo usará pedras numeradas de {BINGO_NUMEROS_INTERVALO[0]} a {BINGO_NUMEROS_INTERVALO[1] - 1}.')

    conexao_redis.sadd(CHAVE_BINGO_NUMEROS, *range(*BINGO_NUMEROS_INTERVALO))


def main():
    global conexao_redis

    print('REDINSGO: Bingo com Redis')
    print()

    with redis.Redis(REDIS_CONEXAO_HOST, REDIS_CONEXAO_PORT) as conexao_redis:
        carregar_numeros_bingo()

if __name__ == '__main__':
    main()