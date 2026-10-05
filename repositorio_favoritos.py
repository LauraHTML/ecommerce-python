import psycopg2

from utils import URL_BANCO

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def criar_lista_favoritos(id_produto, id_usuario):
    query = """
            INSERT INTO favoritos (id_usuario, id_produto, data_criacao)
            VALUES (%s, %s, CURRENT_DATE)
            RETURNING id; 
            """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (id_usuario, id_produto))
            produto_favorito = cursor.fetchone()[0]
            conexao.commit()

            return produto_favorito

def listar_favoritos(id_usuario):
    query = "SELECT * FROM favoritos where id_usuario = %s ORDER BY data_criacao DESC;"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, id_usuario)
            produtos = cursor.fetchall()

            if not produtos:
                return None
            return produtos

def deletar_produto_favoritado(id_produto):
    query = """
    DELETE FROM favoritos WHERE id_produto = %s;
    """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (id_produto,))
            conexao.commit()
            print("Produto excluido da lista de favoritos com sucesso")