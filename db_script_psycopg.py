import psycopg
from psycopg import sql

password = "write your password here!!!" # 비밀번호를 넣어주세요.

# Connect to the PostgreSQL and create a database
conn = psycopg.connect(dbname="postgres", user="postgres", password=password)
conn.autocommit = True
conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("chinook")))
conn.commit()
conn.close()

conn = psycopg.connect(dbname="postgres", user="postgres")

# Create a cursor object
cur = conn.cursor()

# Read the SQL script file
with open('chinook_dump.sql', 'r', encoding="utf8") as file:
    sql_script = file.read()

# Execute the SQL script
cur.execute(sql_script)

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()