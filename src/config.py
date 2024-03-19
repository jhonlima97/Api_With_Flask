from decouple import config

class DevelopmentConfig():
    DEBUG           = True
    MYSQL_HOST      = config('DB_HOST')
    MYSQL_USER      = config('DB_USER')
    MYSQL_PASSWORD  = config('DB_PASS')
    MYSQL_DB        = config('DB_NAME')

