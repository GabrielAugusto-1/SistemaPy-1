import psycopg2

conexao = psycopg2.connect(
       "postgres://postgres.apbkobhfnmcqqzqeeqss:bielpy_123%40@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
)

# conexao = psycopg2.connect(
#     host="localhost",
#     database="pythonteste",
#     user="postgres",
#     password="123456",
#     port="5432"
# )

dbcursor = conexao.cursor()
