import psycopg2

conexao = psycopg2.connect(
   "postgresql://postgres.bvlmnebahunftvabjrph:bielpy_123%40@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
)


# conexao = psycopg2.connect(
#     host="localhost",
#     database="pythonteste",
#     user="postgres",
#     password="123456",
#     port="5432"
# )

dbcursor = conexao.cursor()
