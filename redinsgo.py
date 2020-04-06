import redis


REDIS_CONEXAO_HOST = 'localhost'
REDIS_CONEXAO_PORT = 6379


conexao_redis = None


def main():
    with redis.Redis(REDIS_CONEXAO_HOST, REDIS_CONEXAO_PORT) as conexao_redis:
        pass


if __name__ == '__main__':
    main()