import psycopg2

conexao = psycopg2.connect(
    "postgresql://postgres:bielpy_123%40@db.bvlmnebahunftvabjrph.supabase.co:5432/postgres"
)

# conexao = psycopg2.connect(
#     host="localhost",
#     database="pythonteste",
#     user="postgres",
#     password="123456",
#     port="5432"
# )

dbcursor = conexao.cursor()
