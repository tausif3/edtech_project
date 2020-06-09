import redis

# initiate a redis connection with this config
redis_connection = redis.Redis(host='127.0.0.1', port=6379, db=0)


def setex_jwt_token(username,time,token):
    """
    function is used to perform SETEX operation in redis for a (key,time,value) pair as string data structure
    :param token: string
    :param username: string
    :return:True(1)

    """
    if redis_connection.ping():

        assert token == str(token)
        assert username == str(username)
        assert time == int(time)

        success = redis_connection.setex(username,time,token)
        if success:
            return 1
        else:
            return "(REDIS ERROR) Failed to set username and token try again!"


