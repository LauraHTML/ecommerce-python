import json
from utils import voltar_ao_menu_principal, opcao_invalida, finalizar_app
# verificar se entrada correponse a um padrão especifico
import re
from repositorio_usuario import criar_usuario, login
from repositorio_produto import produtos_em_promocao, repositorio_buscar_produtos
from repositorio_carrinho import adicionar_ao_carrinho

from datetime import datetime, timedelta

email_padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

fundoPadrao = '\033[0;0m'
corPadrao = '\033[1;35m'

# ERRROSS:
class InputError(Exception):
    """Valores de input errados: email já existe, senha curta"""
    pass


def cadastrar_usuario():
    print(f'{fundoPadrao} Cadastro do usuario {corPadrao}')
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
        criar_usuario(nome, senha, email, "cliente")

def logar_usuario():
    try:
        senha: str = input('Insira a sua senha: ').strip()
        if not senha or len(senha) < 6:
            raise InputError('Valor inserido para senha é invalido')

        email: str = input('Insira o seu email: ').strip()
        if not email or not re.match(email_padrao, email):
            raise InputError('Insira um email válido')

        token_autenticado = login(email, senha)
        if token_autenticado != "":
            print(f'Bem vindo(a)')
            return token_autenticado
        else:
            print('Usuário não encontrado')
            return False

    except InputError as erro:
        print(f'Insira um valor válido: {erro}')

# .strip() tira \n

def menu_cliente():
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
                    repositorio_buscar_produtos()
                    voltar_ao_menu_principal()
                case "2":
                    produtos_em_promocao()
                case "3":
                    print('Adicionar ao carrinho')
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
