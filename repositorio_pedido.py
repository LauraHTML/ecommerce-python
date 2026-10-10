import psycopg2
from utils import URL_BANCO

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def itens_carrinho_para_pedido(id_usuario):
    calcular_preco = """
            SELECT SUM(c.quantidade * p.preco_atual)
            FROM carrinho c
                     INNER JOIN produtos p ON p.id = c.id_produto
            WHERE c.id_usuario = %s \
            """
    criar_pedido = "INSERT INTO pedidos (id_usuario, valor_total) VALUES (%s, %s) RETURNING id;"
    itens_pedido = ("""INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario)
                       SELECT %s, c.id_produto, c.quantidade, p.preco_atual
                       FROM carrinho c
                                INNER JOIN produtos p ON p.id = c.id_produto
                       WHERE c.id_usuario = %s;""")
    esvaziar_carrinho = "DELETE FROM carrinho WHERE id_usuario = %s"
    try:
        with conexao:
            with cursor:
                cursor.execute(calcular_preco, (id_usuario,))
                resultado = cursor.fetchone()
                valor_total = round(resultado[0],2) or 0

                cursor.execute(criar_pedido, (id_usuario,valor_total))
                id_pedido = cursor.fetchone()
                cursor.execute(itens_pedido, (id_pedido[0], id_usuario))
                cursor.execute(esvaziar_carrinho, (id_usuario, ))
                conexao.commit()
                return True

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except ValueError:
        print('Valor inválido')

def modificar_status_pedido(id_pedido, id_usuario, status_pedido):
    query = "UPDATE pedidos SET status_pedido = %s WHERE id_pedido = %s AND id_usuario = %s;"
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (status_pedido, id_pedido, id_usuario))
                conexao.commit()

    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
