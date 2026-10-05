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
            INNER JOIN categorias c ON p.id_categoria = c.id WHERE p.id = %s;
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

def reduzir_estoque(id_produto, quantidade_comprada):
    query = """
    UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s AND quantidade > 0
    """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (quantidade_comprada, id_produto))
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"Foram compradas {quantidade_comprada} unidades!")
                return True
            else:
                print("Produto não encontrado.")
                return False

def deletar_produto(id_produto):
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            query = "DELETE FROM produtos WHERE id = %s"
            cursor.execute(query, (id_produto,))
            conexao.commit()
            print("Produto deletado com sucesso")

def atualizar_produto(id_produto, nome= None, descricao= None, preco_atual= None, promocao= None, valor_promocao= None, quantidade= None, id_categoria= None):
    campos_sql = []
    valores = []

    if nome is not None:
        campos_sql.append("nome = %s")
        valores.append(nome)
    if descricao is not None:
        campos_sql.append("descricao = %s")
        valores.append(descricao)
    if promocao is not None:
        campos_sql.append("promocao = %s")
        valores.append(promocao)
    if valor_promocao is not None:
        campos_sql.append("valor_promocao = %s")
        valores.append(valor_promocao)
    if id_categoria is not None:
        campos_sql.append("id_categoria = %s")
        valores.append(id_categoria)
    if quantidade is not None:
        campos_sql.append("quantidade = %s")
        valores.append(quantidade)
    if id_produto is not None:
        campos_sql.append("id_produto = %s")
        valores.append(id_produto)
    if descricao is not None:
        campos_sql.append("descricao = %s")
        valores.append(descricao)
    if preco_atual is not None:
        campos_sql.append("preco_atual = %s")
        valores.append(preco_atual)

    if not campos_sql:
        print("Nenhum dado novo fornecido para atualização.")
        return False
    campos_virgula = ", ".join(campos_sql)
    query = f"UPDATE produtos SET {campos_virgula} WHERE id = %s"
    valores.append(id_produto)

    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, tuple(valores))
            conexao.commit()

            if cursor.rowcount > 0:
                print("Produto atualizado com sucesso!")
                return True
            else:
                print("Nenhum produto encontrado com esse ID.")
                return False

def produtos_em_promocao():
    query = ("""
             SELECT nome, descricao, preco_atual, valor_promocao, quantidade, nome AS nome_categoria
             FROM produtos  WHERE promocao == true;
             """)

    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query)
            produtos_promocao = cursor.fetchall()

            produto_com_promocao = []
            for produto in produtos_promocao:
                produto_com_promocao.append({
                    "id": produto[0],
                    "nome_produto": produto[1],
                    "preco": produto[2],
                    "valor_promocao": produto[3]
                })
            return produto_com_promocao