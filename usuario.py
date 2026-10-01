import json
from utils import voltar_ao_menu_principal, opcao_invalida, finalizar_app
# verificar se entrada correponse a um padrão especifico
import re
from produtos import lista_de_produtos,excluir_produto,adicionar_produto

from datetime import datetime, timedelta

email_padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

fundoPadrao = '\033[0;0m'
corPadrao = '\033[1;35m'

ARQUIVO = "usuarios.json"
SESSAO_ATUAL='sessao_atual.json'

# fazer: verificar se usuario existe, ler usuarios, excluir, atualizar

# ERRROSS:
class InputError(Exception):
    """Valores de input errados: email já existe, senha curta"""
    pass

def ver_usuarios():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return []

usuarios = ver_usuarios()

def salvar_usuario():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return []

def email_existe(email):
    for usuario in usuarios:
        if usuario['email'] == email:
           return True
    return False
# print(email_existe('emailtop'))

def verificar_senha(senha):
    for usuario in usuarios:
        if usuario['senha'] == senha:
            return True
    return False

def buscar_usuario(email, senha):
    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == senha:
            return usuario
    return False

def cadastrar_usuario():
    print(f'{fundoPadrao} Cadastro do usuario {corPadrao}')
    try:
        nome: str = input('Insira o seu nome: ').strip()
        if not nome or not nome.replace(" ", "").isalpha():
            raise InputError('Insira um valor valido para nome: letras e espaços')

        email: str = input('Insira o seu email: ').strip()
        if not email or not re.match(email_padrao, email):
            raise InputError('Insira um email válido')
        if email_existe(email):
           raise InputError('O email inserido já foi cadastrado')

        senha: str = input('Crie uma senha: ').strip()
        if not senha or len(senha) < 6:
            raise InputError('Crie uma senha mais forte')

    except InputError as erro:
        print(f'Valor inserido é invalido: {erro}')
    except Exception as erro:
        print(f'Erro inesperado: {erro}')
    else:
        novo_usuario = {
            "nome": nome,
            "email": email,
            "senha": senha
        }
        usuarios.append(novo_usuario)
        salvar_usuario()

def criar_sessao(usuario_id, usuario_perfil):
    data_expiracao = datetime.now() + timedelta(days=7)
    dados_sessao = {
        "usuario_id": usuario_id,
        "expira_em": data_expiracao.isoformat(),
        "perfil": usuario_perfil
    }
    try:
        with open(SESSAO_ATUAL, "w", encoding="utf-8") as arquivo:
            json.dump(dados_sessao, arquivo)
    except FileNotFoundError:
        print('O arquivo não foi encontrado')

def login():
    try:
        senha: str = input('Insira a sua senha: ').strip()
        if not senha or len(senha) < 6:
            raise InputError('Valor inserido para senha é invalido')

        email: str = input('Insira o seu email: ').strip()
        if not email or not re.match(email_padrao, email):
            raise InputError('Insira um email válido')

        usuario_autenticado = buscar_usuario(email= email, senha= senha)
        if usuario_autenticado:
            criar_sessao(usuario_autenticado['id'], usuario_autenticado['perfil'])
            print(f'Bem vindo(a) {usuario_autenticado['nome']}')
            return usuario_autenticado
        else:
            print('Usuário não encontrado')
            return False

    except InputError as erro:
        print(f'Insira um valor válido: {erro}')

# .strip() tira \n

def ler_sessao():
    try:
        with open(SESSAO_ATUAL, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return False

def verificar_sessao():
    try:
        sessao_atual = ler_sessao()

        if sessao_atual['usuario_id'] != "":
            data_expiracao = datetime.fromisoformat(sessao_atual['expira_em'])
            if data_expiracao > datetime.now():
                # id_usuario_logado = sessao_atual['usuario_id']
                return sessao_atual
        else:
            return False
    except FileNotFoundError:
        print("Nenhuma sessão ativa. Por favor, faça o login.")


def sair_da_conta():
    try:
        dados_sessao = {
            "usuario_id": "",
            "expira_em": "",
            "perfil": ""
        }
        with open(SESSAO_ATUAL, "w", encoding="utf-8") as arquivo:
            json.dump(dados_sessao, arquivo)
    except FileNotFoundError:
        print("Nenhuma sessão ativa.")

def menu_cliente():
    try:
        while True:
            print(f'{corPadrao}1.{fundoPadrao} Ver catálogo')
            print(f'{corPadrao}2.{fundoPadrao} Adicionar ao carrinho')
            print(f'{corPadrao}3.{fundoPadrao} Finalizar compra')
            print(f'{corPadrao}4.{fundoPadrao} Sair\n')
            opcao_usuario = input("Escolha uma opção: ")
            match opcao_usuario:
                case "1":
                    lista_de_produtos()
                    voltar_ao_menu_principal()
                case "2":
                    print('Adicionar ao carrinho')
                case "3":
                    print('finalizar compra')
                case "4":
                    print('Saindo...')
                    sair_da_conta()
                    voltar_ao_menu_principal()
                case _:
                    print("Opção inválida")
                    opcao_invalida()
    except KeyboardInterrupt:
        print('\nPrograma finalizado com sucesso')

def menu_funcionario():
    try:
        while True:
            print(f'{corPadrao}1.{fundoPadrao} Lista de produtos')
            print(f'{corPadrao}2.{fundoPadrao} Adicionar produto')
            print(f'{corPadrao}3.{fundoPadrao} Excluir produto')
            print(f'{corPadrao}4.{fundoPadrao} Sair\n')
            opcao_usuario = input("Escolha uma opção: ")
            match opcao_usuario:
                case "1":
                    lista_de_produtos()
                    voltar_ao_menu_principal()
                case "2":
                    adicionar_produto()
                case "3":
                    excluir_produto()
                case "4":
                    print('Saindo...')
                    sair_da_conta()
                    voltar_ao_menu_principal()
                case _:
                    print("Opção inválida")
    except KeyboardInterrupt:
        print('\nPrograma finalizado com sucesso')