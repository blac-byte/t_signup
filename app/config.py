class Config:
    SECRET_KEY = "hello"  # better to use os.environ
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flaskdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
