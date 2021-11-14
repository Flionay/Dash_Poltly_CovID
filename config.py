class Config(object):
    jsonPath = "/Users/angyi/PycharmProjects/CovIdVis/data/json"
    dataPath = "/Users/angyi/PycharmProjects/CovIdVis/data"
    tencentPath = "/Users/angyi/PycharmProjects/CovIdVis/data/tencent"
    token = open("/Users/angyi/PycharmProjects/CovIdVis/utils/mapbox").read()

    DEBUG = False
    DATABASE_IP = '127.0.0.1'
    DATABASE_PORT = 27017
    DATABASE_USER = 'admin'
    DATABASE_PASS = '123456'


class DevelopmentConfig(Config):
    '''
    开发环境配置
    '''
    DEBUG = True
    DATABASE_IP = '127.0.0.1'
    DATABASE_PORT = '27017'
    DATABASE_USER = 'admin'
    DATABASE_PASS = '123456'


class TestingConfig(Config):
    '''
    测试环境配置
    '''
    DEBUG = False
    DATABASE_IP = '127.0.0.1'
    DATABASE_PORT = '27017'
    DATABASE_USER = 'admin'
    DATABASE_PASS = '123456'
