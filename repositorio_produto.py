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

def buscar_produtos():
    query = "SELECT * FROM produtos ORDER BY id;"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query)
            produtos = cursor.fetchall()

            if not produtos:
                return None

            return produtos

def buscar_produto_por_id(produto_id):
    query = ("""
             SELECT p.nome, p.descricao, p.preco_atual, p.valor_promocao, p.quantidade, c.nome AS nome_categoria 
             FROM produtos p 
            INNER JOIN categorias c ON p.id_categoria = c.id AND WHERE p.id = %s;
             """)
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
                "categoria": resultado[7]
            }
            return produto

def buscar_por_categoria():
    # produtos: p, categorias: c
    query = """
    SELECT p.id, p.nome, p.preco, c.nome AS nome_categoria
    FROM produtos p
        INNER JOIN categorias c ON p.id_categoria = c.id 
    """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query)
            produtos_categorias = cursor.fetchall()

            produto_com_categoria = []
            for linha in produtos_categorias:
                produto_com_categoria.append({
                    "id": linha[0],
                    "nome_produto": linha[1],
                    "preco": linha[2],
                    "categoria": linha[3]
                })
            return produto_com_categoria

def reduzir_estoque(id_produto):
    query = """
    UPDATE produtos SET quantidade = %s - %s WHERE id = %s AND quantidade > 0
    """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (id_produto,))
            conexao.commit()


def deletar_produto(id_produto):
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            query = "DELETE FROM produtos WHERE id = %s"
            cursor.execute(query, (id_produto,))
            conexao.commit()
            print("Produto deletado com sucesso")
