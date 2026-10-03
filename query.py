import psycopg2

url_supabase = "url_conexao"

try:
    conexao = psycopg2.connect(url_supabase)
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()

    print("Conexão com o Supabase feita com sucesso")
    print(usuarios)

except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conexao' in locals():
        conexao.close()