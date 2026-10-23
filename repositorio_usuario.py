import psycopg2
from utils import conexao
import bcrypt
import string
import secrets
import json
import os
from datetime import datetime, timedelta

SESSAO_ATUAL = 'sessao_atual.json'
TOKEN_BYTES = 32

def buscar_usuarios():
    query = """
    SELECT id, nome, email FROM USUARIOS WHERE perfil = 'cliente' """
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query,)
                # Pega o ID que acabou de ser gerado pelo banco
                usuarios = cursor.fetchall()
                conexao.commit()

                return usuarios

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
        return False
    except Exception as erro:
        print(f'Ocorreu um erro ao buscar usuários: {erro}')

def usuarios_pedido_pendente():
    query = """
    SELECT p.id, u.nome, p.data_pedido, p.status_pedido, p.valor_total FROM usuarios u
        INNER JOIN pedidos p ON p.id_usuario = u.id
        WHERE p.status_pedido = 'pendente'
    """
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query,)
                pedidos_pendentes = cursor.fetchall()
                conexao.commit()

                return pedidos_pendentes

    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Ocorreu um erro ao buscar os pedidos pendentes: {erro}')

def gerar_hash(senha_em_texto):
    # Converte a string para bytes
    senha_bytes = senha_em_texto.encode('utf-8')
    # Gera o salt aleatório
    salt = bcrypt.gensalt(10)
    # Cria o hash final
    senha_hash = bcrypt.hashpw(senha_bytes, salt)
    return senha_hash.decode('utf-8')

def verificar_senha(senha_texto, senha_hash):
    senha_texto_byte = senha_texto.encode('utf-8')
    if isinstance(senha_hash, memoryview):
        senha_hash_byte = senha_hash.tobytes()
    elif isinstance(senha_hash, str):
        senha_hash_byte = senha_hash.encode('utf-8')
    elif isinstance(senha_hash, bytes):
        senha_hash_byte = senha_hash
    else:
        raise ValueError('O hash de senha armazenado está em um formato inválido.')

    if not senha_hash_byte.startswith((b'$2a$', b'$2b$', b'$2y$')):
        raise ValueError('O hash de senha armazenado não é um hash bcrypt válido.')

    return bcrypt.checkpw(senha_texto_byte, senha_hash_byte)

def criar_usuario(nome, email, senha, perfil):
    senha_usuario = gerar_hash(senha)
    # Insere um usuário no banco e retorna o ID gerado automaticamente
    query = """
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (%s, %s, %s, %s)
            RETURNING id; 
            """
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (nome, email, senha_usuario, perfil))
                # Pega o ID que acabou de ser gerado pelo banco
                novo_id = cursor.fetchone()[0]
                conexao.commit()

                return novo_id
    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')

def buscar_usuario(id_usuario):
    # Busca um usuário pelo ID e retorna um dicionário
    query = "SELECT id, nome, email, perfil FROM usuarios WHERE id = %s;"
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (id_usuario,))
                resultado = cursor.fetchone()

                # Se não encontrar ninguém retorna None
                if not resultado:
                    return None
                # Se encontrar converte a tupla do banco de volta para um dicionário
                usuario = {
                    "id": resultado[0],
                    "nome": resultado[1],
                    "email": resultado[2],
                    "perfil": resultado[3]
                }
                return usuario
    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')

def atualizar_usuario(id_usuario, nome=None, email=None, senha=None):
    campos_sql = []
    valores = []
    if nome is not None:
        campos_sql.append("nome = %s")
        valores.append(nome)
    if email is not None:
        campos_sql.append("email = %s")
        valores.append(email)
    if senha is not None:
        campos_sql.append("senha = %s")
        valores.append(senha)

    if not campos_sql:
        print("Nenhum dado novo fornecido para atualização.")
        return False
    campos_virgula = ", ".join(campos_sql)
    query = f"UPDATE usuarios SET {campos_virgula} WHERE id = %s"
    valores.append(id_usuario)

    try:
        with  conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, tuple(valores))
                conexao.commit()

                if cursor.rowcount > 0:
                    print("Usuário atualizado com sucesso no banco de dados!")
                    return True
                else:
                    print("Nenhum usuário encontrado com esse ID.")
                    return False
    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')

def deletar_usuario(id_usuario):
    try:
        with conexao:
            with conexao.cursor() as cursor:
                query = "DELETE FROM usuarios WHERE id = %s"
                cursor.execute(query, (id_usuario,))
                conexao.commit()
                print("Usuário deletado com sucesso")
    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')

def gerar_token():
    token = secrets.token_urlsafe(TOKEN_BYTES)
    return token

# data = datetime.now()
# print(data)

def criar_sessao_json(id_usuario, usuario_perfil):
    data_expiracao = datetime.now() + timedelta(days=3)
    dados_sessao = {
        "id_usuario": id_usuario,
        "expira_em": data_expiracao.isoformat(),
        "perfil": usuario_perfil
    }
    try:
        with open(SESSAO_ATUAL, "w", encoding="utf-8") as arquivo:
            json.dump(dados_sessao, arquivo)
    except FileNotFoundError:
        print('Usuário não logado')

def ler_sessao():
    try:
        with open(SESSAO_ATUAL, "r", encoding="utf-8") as arquivo:
            sessao_atual = json.load(arquivo)
            return sessao_atual
    except FileNotFoundError:
        print('Usuário não logado')
        return False

def excluir_sessao(id_usuario):
    query = "DELETE FROM sessoes WHERE id_usuario = %s;"
    try:
        os.remove(SESSAO_ATUAL)
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query,(id_usuario,))
        print("Você saiu da sua conta com sucesso")

    except FileNotFoundError:
        print("Nenhuma sessão ativa")
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado ao sair da conta: {erro}')

# validar credenciais
def login(email, senha):
    try:
        query = """
            SELECT id, senha, perfil
            FROM public.usuarios
            WHERE email = %s;
        """
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (email,))
                usuario_encontrado = cursor.fetchone()
                if usuario_encontrado is None:
                    print('O email está incorreto, nenhum usuário encontrado')
                    return False

                id_usuario, senha_hash, perfil = usuario_encontrado
                try:
                    senha_correta = verificar_senha(
                        senha_texto=senha,
                        senha_hash=senha_hash
                    )
                except ValueError as erro:
                    print(f'Não foi possível validar a senha cadastrada: {erro}')
                    print('Redefina a senha ou cadastre a conta novamente.')
                    return False

                if not senha_correta:
                    print('A senha digitada está incorreta')
                    return False

                token = gerar_token()

                criar_sessao = "INSERT INTO sessoes (id_usuario, token_sessao) VALUES (%s, %s);"
                cursor.execute(criar_sessao, (id_usuario, token))
                conexao.commit()
                criar_sessao_json(id_usuario, perfil)
                return id_usuario
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro ao logar: {erro}')

def validar_sessao():
    query = "SELECT id_usuario, token_sessao, data_criacao FROM sessoes WHERE id_usuario = %s;"
    sessao_json = ler_sessao()
    if not sessao_json:
        return False
    id_usuario = sessao_json["id_usuario"]
    data_expiracao = datetime.fromisoformat(sessao_json["expira_em"])
    data_atual = datetime.now()
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (id_usuario,))
                sessao_encontrada = cursor.fetchone()

                if data_expiracao < data_atual:
                    print("Sessão expirada. Faça login novamente")
                    excluir_sessao(id_usuario)
                    return False
                if id_usuario != sessao_encontrada[0]:
                    return False
                else:
                    return sessao_json
    except FileNotFoundError:
        print("Nenhuma sessão ativa. Por favor, faça o login.")
        return False
    except TypeError as erro:
        print(f"Houve um erro ao validar a sessão: {erro}")
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
        return False
    except Exception as erro:
        print(f'Erro ao validar sessão: {erro}')
        return False

def sair_da_conta(id_usuario):
    query = "DELETE FROM sessoes where id = %s"
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (id_usuario,))
                conexao.commit()

    except TypeError:
        print('Valor inválido para a operação')
    except psycopg2.Error as erro:
        print(f'Erro no banco de dados: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
