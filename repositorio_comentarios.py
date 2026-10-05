import psycopg2

from utils import URL_BANCO

conexao = psycopg2.connect(URL_BANCO)
cursor = conexao.cursor()

def criar_comentario(id_usuario, id_produto, texto, promocao, valor_nota, img_url, data_criacao):
    query = """
            INSERT INTO comentarios (id_usuario, id_produto, texto, promocao, valor_nota, img_url, data_criacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id; 
            """
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (id_usuario, id_produto, texto, promocao, valor_nota, img_url, data_criacao))
            comentario_id = cursor.fetchone()[0]
            conexao.commit()

            return comentario_id

def ordenar_comentarios():
    query = "SELECT * FROM comentarios ORDER BY data_criacao DESC;"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query)
            comentarios = cursor.fetchall()
            if not comentarios:
                return None
            return comentarios

def atualizar_comentario(id_comentario, id_produto, valor_nota, texto=None, img_url=None):
    campos_sql = []
    valores = []
    if not id_comentario or not id_produto or not valor_nota:
        return False
    campos_sql.append("data_criacao = CURDATE()")
    if texto is not None:
        campos_sql.append("nome = %s")
        valores.append(texto)
    if img_url is not None:
        campos_sql.append("email = %s")
        valores.append(img_url)


    if not campos_sql:
        print("Nenhum dado novo fornecido para atualização.")
        return False

    campos_virgula = ", ".join(campos_sql)
    query = f"UPDATE comentarios SET {campos_virgula} WHERE id = %s"
    valores.append([id_comentario, id_produto])

    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, tuple(valores))
            conexao.commit()

            if cursor.rowcount > 0:
                print("Comentário atualizado com sucesso")
                return True
            else:
                print("Nenhum comentário encontrado com esse ID.")
                return False

def deletar_comentario(id_comentario):
    query = "DELETE FROM comentarios WHERE id = %s"
    with psycopg2.connect(URL_BANCO) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query, (id_comentario,))
            conexao.commit()
            print("Comentário deletado com sucesso")