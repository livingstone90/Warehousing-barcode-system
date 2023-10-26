import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="warehouse_items",
    user="postgres",
    password="123@Livo",
)
