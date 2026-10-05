import psycopg2
from utils import URL_BANCO

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def criar_usuario(nome, email, senha, perfil):
    # Insere um usuário no banco e retorna o ID gerado automaticamente
    query = """
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (%s, %s, %s, %s)
            RETURNING id; 
            """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (nome, email, senha, perfil))
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
            print("Usuário deletado.")