import psycopg2

conn = psycopg2.connect(
    host="localhost",   # ← IP Docker
    port=5436,
    user="user",
    password="password",
    dbname="elec_load"
)

print("CONNECTED")
conn.close()