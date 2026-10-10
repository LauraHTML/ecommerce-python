import psycopg2
from utils import URL_BANCO
import bcrypt
import string
import random

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()


def gerar_hash(senha_em_texto):
    # Converte a string para bytes
    senha_bytes = senha_em_texto.encode('utf-8')
    # Gera o salt aleatório
    salt = bcrypt.gensalt(10)
    # Cria o hash final
    senha_hash = bcrypt.hashpw(senha_bytes, salt)
    return senha_hash


def verificar_senha(senha_texto, senha_hash):
    senha_texto_byte = senha_texto.encode('utf-8')
    senha_hash_byte = senha_hash.encode('utf-8')
    return bcrypt.checkpw(senha_texto_byte, senha_hash_byte)

def criar_usuario(nome, email, senha, perfil):
    senha_usuario = gerar_hash(senha)
    # Insere um usuário no banco e retorna o ID gerado automaticamente
    query = """
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (%s, %s, %s, %s)
            RETURNING id; 
            """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (nome, email, senha_usuario, perfil))
            # Pega o ID que acabou de ser gerado pelo banco
            novo_id = cursor.fetchone()[0]
            conexao.commit()

            return novo_id

def buscar_usuario_por_id(id_usuario):
    # Busca um usuário pelo ID e retorna um dicionário
    query = "SELECT id, nome, email, perfil FROM usuarios WHERE id = %s;"
    with psycopg2.connect(URL_BANCO) as conexao:
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

    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, tuple(valores))
            conexao.commit()

            if cursor.rowcount > 0:
                print("Usuário atualizado com sucesso no banco de dados!")
                return True
            else:
                print("Nenhum usuário encontrado com esse ID.")
                return False

def deletar_usuario(id_usuario):
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (id_usuario,))
            conexao.commit()
            print("Usuário deletado com sucesso")

def gerar_token(size=6, chars=string.ascii_uppercase + string.digits):
    # ascii_uppercase: todas as letras em maiusculo
    # string.digits: uma string com numeros
    # chars: lista de caracteres contendo numeros e letras
    # random.choice: resgata um caracter aleatorio
    # join: junta a string
    return ''.join(random.choice(chars) for _ in range(size))

# print(gerar_token())

# def criar_sessao(id_usuario):
#     query = "INSERT INTO sessoes (id_usuario, token_sessao) VALUES (%s, %s);"
#     token = gerar_token()
#     try:
#         with psycopg2.connect(URL_BANCO) as conexao:
#             with conexao.cursor() as cursor:
#                 cursor.execute(query, (id_usuario, token))
#                 conexao.commit()
#     except Exception as e:
#         print(f'Error ao criar sessão: {e}')

# validar credenciais
def login(email, senha):
    try:
        query = "SELECT * FROM public.usuarios WHERE email = %s ;"
        with psycopg2.connect(URL_BANCO) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (email,))
                usuario_encontrado = cursor.fetchone()
                if usuario_encontrado is None:
                    print('O email está incorreto, nenhum usuário encontrado')
                    return None

            senha_hash = usuario_encontrado[4]
            if verificar_senha(senha_texto=senha, senha_hash =senha_hash):
                id_usuario = usuario_encontrado[0]
                token = gerar_token()

                criar_sessao = "INSERT INTO sessoes (id_usuario, token_sessao) VALUES (%s, %s);"
                cursor.execute(criar_sessao, (id_usuario, token))
                return token
            else:
                print('A senha digitada está incorreta')
            conexao.commit()

    except Exception as e:
        print(f'Erro ao logar: {e}')

def validar_sessao(token):
    query = "SELECT * FROM sessoes WHERE token_sessao = %s;"

    try:
        with psycopg2.connect(URL_BANCO) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, (token,))

                sessao_encontrada = cursor.fetchone()

                if sessao_encontrada is None:
                    print('O usuário não está logado')
                usuario_id = sessao_encontrada[1]
                return usuario_id
    except Exception as e:
        print(f'Erro ao validar sessão: {e}')
        return None