import psycopg2

from utils import URL_BANCO

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def criar_produto(nome, descricao, preco_atual, promocao, valor_promocao, quantidade, id_categoria):
    query = """
    INSERT INTO produtos (nome, descricao, preco_atual, promocao, valor_promocao, quantidade, id_categoria)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id;
    """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (nome, descricao, preco_atual, promocao, valor_promocao, quantidade, id_categoria))

            produto_id = cursor.fetchone()[0]
            conexao.commit()

            return produto_id

def buscar_produto_por_id(produto_id):
    query = "SELECT nome, descricao, preco_atual, valor_promocao, quantidade FROM produtos WHERE id = %s;"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query,(produto_id,))
            resultado = cursor.fetchone()

            if not resultado:
                return None
            produto = {
                "id": resultado[0],
                "nome": resultado[1],
                "descricao": resultado[2],
                "preco_atual": resultado[3],
                "promocao": resultado[4],
                "valor_promocao": resultado[5],
                "quantidade": resultado[6],
                "id_categoria": resultado[7]
            }
            return produto
