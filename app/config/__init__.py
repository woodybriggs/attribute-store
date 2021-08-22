import os

DATABASE_URL = os.getenv('DATABASE_URL', "mysql+aiomysql://root:example@0.0.0.0:3306/attribute")