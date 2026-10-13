import psycopg2

from utils import cursor, conexao

def criar_lista_favoritos(id_produto, id_usuario):
    query = """
            INSERT INTO favoritos (id_usuario, id_produto, data_criacao)
            VALUES (%s, %s, CURRENT_DATE)
            RETURNING id; 
            """
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_usuario, id_produto))
                produto_favorito = cursor.fetchone()[0]
                conexao.commit()

                return produto_favorito
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')

def listar_favoritos(id_usuario):
    query = "SELECT * FROM favoritos where id_usuario = %s ORDER BY data_criacao DESC;"
    try:
        with conexao:
            with cursor:
                cursor.execute(query, id_usuario)
                produtos = cursor.fetchall()

                if not produtos:
                    return None
                return produtos
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')

def deletar_produto_favoritado(id_produto):
    query = """
    DELETE FROM favoritos WHERE id_produto = %s;
    """
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_produto,))
                conexao.commit()
                print("Produto excluido da lista de favoritos com sucesso")
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')