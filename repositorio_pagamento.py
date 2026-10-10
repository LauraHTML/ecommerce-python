import psycopg2
import string
import random

from utils import URL_BANCO
from repositorio_pedido import modificar_status_pedido

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def listar_metodos_pagamento(id_usuario):
    query = """
    SELECT tipo, final_cartao FROM meio_de_pagamento WHERE id_usuario = %s;
    """
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_usuario,))
                metodos_pagamento = cursor.fetchall()

                if metodos_pagamento:
                    for metodo_pagamento in metodos_pagamento:
                        meu_metodo ={
                            'tipo': metodo_pagamento[1],
                            'final_cartao': metodo_pagamento[2],
                        }
                    return meu_metodo
                print('Não há nenhum método de pagamento salvo')
                return []

    except TypeError as erro:
        print(f'Valor inserido é invalido: {erro}')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')

def modificar_status_pagamento(id_pedido, id_usuario, status_pagamento):
    query = "UPDATE pagamento SET status_pagamento = %s WHERE id_pedido = %s AND id_usuario = %s;"
    try:
        with conexao:
            with cursor:
                cursor.execute(query, (status_pagamento, id_pedido, id_usuario))
                conexao.commit()

    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')

def simular_pagamento(final_cartao_selecionado, id_usuario):
    query = "SELECT final_cartao FROM meio_de_pagamento WHERE id_usuario = %s;"

    try:
        with conexao:
            with cursor:
                cursor.execute(query, (id_usuario,))
                final_cartao_banco = cursor.fetchone()
                print(final_cartao_banco)

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except TypeError as erro:
        print(f'Valor inserido é invalido: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')

# simular_pagamento(1234, 1)

def pagamento_cartao(id_usuario, id_pedido, metodo_pagamento, token_recebido):
    token_usuario = "SELECT token FROM meio_de_pagamento WHERE id_usuario = %s;"
    query = """
    INSERT INTO pagamento (id_usuario, id_pedido, metodo_pagamento) 
    VALUES (%s, %s, %s)
    RETURNING id
    """
    if id_usuario is None or id_pedido is None or metodo_pagamento is None:
        print('Um dos valores está faltando: pedido, método de pagamento, usuário')
        return
    try:
        with conexao:
            with cursor:
                cursor.execute(token_usuario, (id_usuario,))
                token_banco = cursor.fetchone()

                if token_banco == token_recebido:
                    cursor.execute(query, (id_usuario, id_pedido, metodo_pagamento))
                    modificar_status_pagamento(id_pedido, id_usuario, "aprovado")
                    conexao.commit()
                cursor.execute(query, (id_usuario, id_pedido, metodo_pagamento))
                modificar_status_pagamento(id_pedido, id_usuario, "erro")
                conexao.commit()

    except TypeError as erro:
        print(f'Valor inserido é invalido: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
        modificar_status_pagamento(id_pedido, id_usuario, "erro")

def gerar_codigo_pix(size=8, chars=string.ascii_uppercase + string.digits):
    # ascii_uppercase: todas as letras em maiusculo
    # string.digits: uma string com numeros
    # chars: lista de caracteres contendo numeros e letras
    # random.choice: resgata um caracter aleatorio
    # join: junta a string
    return ''.join(random.choice(chars) for _ in range(size))

# def pagamento_pix(id_usuario, id_pedido, entrada_usuario):
#     codigo_pix = gerar_codigo_pix()
#     pagamento_por_pix = """
#             INSERT INTO pagamento (id_usuario, id_pedido, metodo_pagamento, codigo_pagamento, data_expiração)
#             VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP + interval %s)
#             RETURNING id
#             """
#     if id_usuario is None or id_pedido is None:
#         print('Um dos valores está faltando: pedido, usuário')
#         return
#
#     try:
#         if entrada_usuario == "s":
#             with conexao:
#                 with cursor:
#                     cursor.execute(pagamento_por_pix, (id_usuario, id_pedido, "pix", codigo_pix))
#                     modificar_status_pagamento(id_pedido, id_usuario, "aprovado")
#                     modificar_status_pedido(id_pedido, id_usuario, "pago")
#                     conexao.commit()
#         else:
#             with conexao:
#                 with cursor:
#                     cursor.execute(pagamento_por_pix, (id_usuario, id_pedido, "pix", ''))
#                     modificar_status_pagamento(id_pedido, id_usuario, "pendente")
#                     conexao.commit()
#
#     except Exception as erro:
#         print(f'Erro inesperado: {erro}')
#         modificar_status_pagamento(id_pedido, id_usuario, "erro")
#
# pagamento_pix(1,7,"s")