fundoPadrao = '\033[0;0m'
corNumerosPadrao = '\033[1;35m'

from utils import voltar_ao_menu_principal
from usuario import login
from usuario import cadastrar_usuario
from usuario import verificar_sessao, criar_sessao, menu_cliente, menu_funcionario
from produtos import lista_de_produtos

def finalizar_app():
    print('Finalizar app')

def opcao_invalida():
    print('Opção inválida!\n')
    voltar_ao_menu_principal()

def menu_usuario():
    # retorna a sessão atual
    dados_usuario_logado = verificar_sessao()
    if dados_usuario_logado['usuario_id'] != "":
        if dados_usuario_logado['perfil'] == "cliente":
            menu_cliente()
        else:
            menu_funcionario()
    else:
        menu_principal()

def menu_principal():
    try:
        while True:
            print(f'{corNumerosPadrao}1.{fundoPadrao} Fazer login')
            print(f'{corNumerosPadrao}2.{fundoPadrao} Fazer cadastro')
            print(f'{corNumerosPadrao}3.{fundoPadrao} Ver produtos')
            print(f'{corNumerosPadrao}4.{fundoPadrao} Sair\n')

            escolha_menu = input("Escolha uma opção: ")
            match escolha_menu:
                case "1":
                    usuario = login()
                    criar_sessao(usuario_id=usuario['id'], usuario_perfil=usuario['perfil'])
                case "2":
                    cadastrar_usuario()
                    menu_usuario()
                case "3":
                    lista_de_produtos()
                case "4":
                    print("Saindo...")
                    finalizar_app()
                case _:
                    finalizar_app()
                    opcao_invalida()
    except KeyboardInterrupt:
        print('\nPrograma finalizado com sucesso')

def main():
    print('E-commerce python')
    menu_usuario()

if __name__ == '__main__':
    main()