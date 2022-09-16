import os, pymysql.cursors

# save db login vars to variables
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_DATABASE_NAME")


# define the database connection function
def connect_to_db():
    return pymysql.connect(host=db_host,
                           user=db_user,
                           password=db_pass,
                           database=db_name,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

