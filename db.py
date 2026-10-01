import sqlite3

conexao = sqlite3.connect('banco_de_dados.db')
cursor = conexao.cursor()

# criar tabela de produtos
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    preco DECIMAL(4, 2) NOT NULL,
    promocao BOOLEAN NOT NULL,
    valor_promocao INTERGER NOT NULL
    )
    '''
)
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    idade INTERGER NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(6) NOT NULL,
    perfil TEXT NOT NULL CHECK(perfil IN ("perfil","admin")) DEFAULT "cliente",
    celular INTERGER(11) NOT NULL
    )
    '''
)

# cursor.execute('''
#     INSERT INTO produtos (nome, descricao, preco, promocao, valor_promocao) VALUES ("Prato","prato de cerâmica azul",70.00,false,0)
# ''')
# cursor.execute('''
#     INSERT INTO usuarios  (nome, idade, email, senha, celular) VALUES ("Rayssa Lavínia",19,"rayssa@gmail.com","senha123", 11435672342)
# ''')

conexao.commit()
conexao.close()
# cursor.execute("SELECT * FROM produtos")
# produtos_pesquisa = cursor.fetchone()
# cursor.execute("SELECT * FROM usuarios")
# usuarios_pesquisa = cursor.fetchone()
# print(f'Produto: {produtos_pesquisa}\n {usuarios_pesquisa}')