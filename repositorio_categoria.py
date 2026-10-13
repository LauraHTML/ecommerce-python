import psycopg2

from utils import cursor, conexao

def criar_categoria(nome, descricao):
    query = """
    INSERT INTO categorias (nome, descricao) values (%s,%s) RETURNING id;
    """
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (nome, descricao))
                categoria_id = cursor.fetchone()[0]
                conexao.commit()

                return categoria_id

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
        return None
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
        return None

def buscar_categorias():
    query = "SELECT * FROM categorias ORDER BY id;"
    try:
        with conexao:
            with cursor:
                cursor.execute(query)
                categorias = cursor.fetchall()

                if not categorias:
                    return None

                return categorias
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
        return []
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
        return []

def buscar_categoria_por_id(id_categoria):
    query = "SELECT (nome, descricao) FROM categorias WHERE id = %s;"
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_categoria,))
                categoria = cursor.fetchone()
                if not categoria:
                    return None
                return categoria
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
        return None
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
        return None

def deletar_categoria(id_categoria):
    try:
        with conexao:
            with cursor:
                query = "DELETE FROM categorias WHERE id = %s"
                cursor.execute(query, (id_categoria,))
                conexao.commit()
                print("Categoria deletada com sucesso")
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')