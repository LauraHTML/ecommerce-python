import json
from utils import voltar_ao_menu_principal, opcao_invalida, finalizar_app
# verificar se entrada correponse a um padrão especifico
import re
from repositorio_usuario import criar_usuario, login, validar_sessao, ler_sessao
from repositorio_produto import produtos_em_promocao, repositorio_buscar_produtos
from repositorio_carrinho import repositorio_adicionar_ao_carrinho

from datetime import datetime, timedelta

email_padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

fundoPadrao = '\033[0;0m'
corPadrao = '\033[1;35m'

# ERRROSS:
class InputError(Exception):
    """Valores de input errados: email já existe, senha curta"""
    pass

def listar_produtos():
    produtos = repositorio_buscar_produtos()
    print(f'{corPadrao}Produtos:{fundoPadrao}')
    for produto in produtos:
        produto = {
            "produto": produto[0],
            "nome": produto[1],
            "descrição": produto[2],
            "preço": produto[3],
            "categoria": produto[4],
        }
        print(produto)

def cadastrar_usuario():
    print(f'{fundoPadrao}Cadastro do usuario {corPadrao}')
    try:
        nome: str = input('Insira o seu nome: ').strip()
        if not nome or not nome.replace(" ", "").isalpha():
            raise InputError('Insira um valor valido para nome: letras e espaços')

        email: str = input('Insira o seu email: ').strip()
        if not email or not re.match(email_padrao, email):
            raise InputError('Insira um email válido')

        senha: str = input('Crie uma senha: ').strip()
        if not senha or len(senha) < 6:
            raise InputError('Crie uma senha mais forte')

    except InputError as erro:
        print(f'Valor inserido é invalido: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
    else:
        criar_usuario(nome, email, senha, "cliente")

def logar_usuario():
    try:
        senha: str = input('Insira a sua senha: ').strip()
        if not senha or len(senha) < 6:
            raise InputError('Valor inserido para senha é invalido')

        email: str = input('Insira o seu email: ').strip()
        if not email or not re.match(email_padrao, email):
            raise InputError('Insira um email válido')

        id_usuario = login(email, senha)
        if id_usuario:
            print(f'Bem vindo(a) {email}')
            return id_usuario
        else:
            print('Usuário não encontrado')
            return False

    except InputError as erro:
        print(f'Insira um valor válido: {erro}')

def adicionar_ao_carrinho(id_usuario):
    try:
        print(f'{corPadrao}Adicionar ao carrinho{fundoPadrao}')
        listar_produtos()
        comprar_produto = input("Digite o númerodo produto: ")
        quantidade = int(input("Quantos você vai comprar?: "))
        repositorio_adicionar_ao_carrinho(id_usuario=id_usuario, id_produto=comprar_produto, quantidade=quantidade)

    except Exception as erro:
        print(f"Erro ao adicionar ao carrinho; {erro}")

def menu_cliente(id_usuario):
    try:
        while True:
            print(f'{corPadrao}1.{fundoPadrao} Ver catálogo')
            print(f'{corPadrao}2.{fundoPadrao} Produtos em promoção')
            print(f'{corPadrao}3.{fundoPadrao} Adicionar ao carrinho')
            print(f'{corPadrao}4.{fundoPadrao} Finalizar compra')
            print(f'{corPadrao}5.{fundoPadrao} Sair\n')
            opcao_usuario = input("Escolha uma opção: ")
            match opcao_usuario:
                case "1":
                    listar_produtos()
                    voltar_ao_menu_principal()
                case "2":
                    produtos_em_promocao()
                case "3":
                    adicionar_ao_carrinho(id_usuario)
                case "4":
                    print('finalizar compra')
                case "5":
                    print('Saindo...')
                    # sair_da_conta()
                    voltar_ao_menu_principal()
                case _:
                    print("Opção inválida")
                    opcao_invalida()
    except KeyboardInterrupt:
        print('\nPrograma finalizado com sucesso')
