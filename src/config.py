class DevelopmentConfig():
    DEBUG           = True
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'root'
    MYSQL_PASSWORD  = 'ADMINPHP'
    MYSQL_DB        = 'api_flask'

config = {
    'development': DevelopmentConfig
}