fundoPadrao = '\033[0;0m'
corNumerosPadrao = '\033[1;35m'

from utils import voltar_ao_menu_principal
from usuario import logar_usuario, cadastrar_usuario, menu_cliente
from repositorio_usuario import validar_sessao

def finalizar_app():
    print('Finalizar app')

def opcao_invalida():
    print('Opção inválida!\n')
    voltar_ao_menu_principal()

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
                    id_usuario = logar_usuario()
                    menu_cliente(id_usuario)
                case "2":
                    cadastrar_usuario()
                case "3":
                    print("produtos")
                case "4":
                    print("Saindo...")
                    finalizar_app()
                case _:
                    finalizar_app()
                    opcao_invalida()
    except KeyboardInterrupt:
        print('\nPrograma finalizado com sucesso')

def main():
    sessao_atual = validar_sessao()
    if sessao_atual:
        print('E-commerce python')
        menu_cliente(sessao_atual["id_usuario"])
    else:
        menu_principal()

if __name__ == '__main__':
    main()