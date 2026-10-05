import psycopg2

from utils import URL_BANCO

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def criar_categoria(nome, descricao):
    query = """
    INSERT INTO categorias (nome, descricao) values (%s,%s) RETURNING id;
    """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (nome, descricao))
            categoria_id = cursor.fetchone()[0]
            conexao.commit()

            return categoria_id

def buscar_categorias():
    query = "SELECT * FROM categorias ORDER BY id;"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query)
            categorias = cursor.fetchall()

            if not categorias:
                return None

            return categorias

def buscar_categoria_por_id(id_categoria):
    query = "SELECT (nome, descricao) FROM categorias WHERE id = %s;"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (id_categoria,))
            categoria = cursor.fetchone()
            if not categoria:
                return None
            return categoria

def deletar_categoria(id_categoria):
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            query = "DELETE FROM categorias WHERE id = %s"
            cursor.execute(query, (id_categoria,))
            conexao.commit()
            print("Categoria deletada com sucesso")