from utils import conexao, cursor
import psycopg2
from repositorio_produto import reduzir_estoque

def mostrar_carrinho(usuario_id):
    query = """SELECT c.quantidade, c.data_adicao, c.id_produto, p.nome, p.preco_atual, p.quantidade AS estoque
               FROM carrinho c
               INNER JOIN produtos p ON p.id= c.id_produto
                WHERE c.id_usuario = %s
            """
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (usuario_id,))
                carrinhos = cursor.fetchall()

                for carrinho in carrinhos:
                    carrinho = {
                        "quantidade": carrinho[0],
                        "data_adicao": carrinho[1],
                        "id_produto": carrinho[2],
                        "nome do produto": carrinho[3],
                        "preco_atual": carrinho[4],
                        "estoque do produto": carrinho[5],
                    }
                print(carrinho)
                conexao.commit()

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')

# mostrar_carrinho(1)

def adicionar_ao_carrinho(id_usuario, id_produto, quantidade):
    query = """INSERT INTO carrinho (id_usuario, id_produto, quantidade) VALUES (%s, %s, %s)
            ON CONFLICT (id_usuario, id_produto)
            DO UPDATE SET quantidade = carrinho.quantidade + EXCLUDED.quantidade"""
    try:
        if id_usuario is None or id_produto is None:
            print('Nenhum id de usuário ou produto recebido')
        if quantidade <= 0:
            print('Quantidade de produtos inválido')
        with conexao:
             with cursor:
                 cursor.execute(query, (id_usuario, id_produto, quantidade))
                 conexao.commit()

        reduzir_estoque(id_produto = id_produto, quantidade_retirada= quantidade)
        return True

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except ValueError:
        print('O valor inserido não é válido')

def remover_do_carrinho(id_usuario, id_produto):
    query = """DELETE FROM carrinho WHERE id_usuario = %s AND id_produto = %s"""
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_usuario, id_produto))
                conexao.commit()
                print('Item retirado do carrinho com sucesso')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')

def esvaziar_carrinho(id_usuario):
    resposta_usuario = input('Você tem certeza que quer excluir todos os itens do seu carrinho? (S/N): ').lower().startswith('s')
    query = "DELETE FROM carrinho WHERE id_usuario = %s"
    try:
        if resposta_usuario:
            with conexao:
                with cursor:
                    cursor.execute(query, (id_usuario,))
                    conexao.commit()
                    print('Carrinho esvaziado com sucesso')

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except ValueError:
        print('Valor inválido')

def calcular_subtotal_carrinho(id_usuario):
    query = """
    SELECT SUM(c.quantidade * p.preco_atual)
               FROM carrinho c
               INNER JOIN produtos p ON p.id= c.id_produto
                WHERE c.id_usuario = %s
    """
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_usuario,))
                calculo_subtotal_compra = cursor.fetchone()
                subtotal_compra = round(calculo_subtotal_compra[0], 2)

                if subtotal_compra is None:
                    print('O carrinho está vazio')
                print(f'O subtotal da sua compra até agora é: {subtotal_compra}')
                conexao.commit()

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except ValueError:
        print('Valor inválido')

calcular_subtotal_carrinho(1)