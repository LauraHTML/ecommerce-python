from dotenv import load_dotenv
import os

load_dotenv()

def voltar_ao_menu_principal():
    input('\nPressione uma tecla para voltar ao menu: ')
    from main import main
    main()

def finalizar_app():
    print('Finalizar app')

def opcao_invalida():
    print('Opção inválida!\n')
    voltar_ao_menu_principal()

URL_BANCO = os.getenv("URL_SUPABASE")