from utils import voltar_ao_menu_principal, opcao_invalida, finalizar_app
from repositorio_produto import repositorio_criar_produto, repositorio_buscar_produtos, repositorio_deletar_produto, repositorio_atualizar_produto
from repositorio_usuario import usuarios_pedido_pendente
from repositorio_pedido import modificar_status_pedido, buscar_pedido

fundoPadrao = '\033[0;0m'
corPadrao = '\033[1;35m'

# ERRROSS:
class InputError(Exception):
    """Valores de input errados: email já existe, senha curta"""
    pass

def criar_produto():
    try:
        print('Adicione um produto:')
        nome_produto = input('Nome do produto: ')
        preco = float(input('Preço do produto: '))
        descricao = input('Descrição do produto: ')
        promocao = input('O produto está com desconto? (s/n): ').lower().startswith('s')
        verificacao_desconto = lambda promocao: float(input('Desconto do produto (em porcentagem): ')) if promocao == True else 0
        estoque = int(input('Estoque do produto: '))
        id_categoria = int(input('ID da categoria: '))

        repositorio_criar_produto(nome=nome_produto, preco_atual=preco, descricao=descricao, promocao=promocao, valor_promocao=verificacao_desconto, quantidade=estoque, id_categoria=id_categoria)
    except ValueError as erro:
        print(f'Erro ao ler o valor do produto: {erro}')
        opcao_invalida()
    except InputError as erro:
        print(f'Erro ao criar produto: {erro}')
        opcao_invalida()

def excluir_produto():
    try:
        repositorio_buscar_produtos()
        id_produto = int(input('Insira o ID do produto que vai ser excluido: '))
        repositorio_deletar_produto(id_produto)
    except ValueError as erro:
        print(f'Erro ao ler o valor do produto: {erro}')
        opcao_invalida()
    except InputError as erro:
        print(f'Erro ao criar produto: {erro}')
        opcao_invalida()
    except Exception as erro:
        print(f'Erro ao deletar produto: {erro}')
        opcao_invalida()

def atualizar_produto():
    try:
        print('Atualizar um produto:')
        id_produto = int(input('Insira o ID do produto: '))
        nome_produto = input('Nome do produto: ')
        preco = float(input('Preço do produto: '))
        descricao = input('Descrição do produto: ')
        promocao = input('O produto está com desconto? (s/n): ').lower().startswith('s')
        verificacao_desconto = lambda promocao: float(
            input('Desconto do produto (em porcentagem): ')) if promocao == True else 0
        estoque = int(input('Estoque do produto: '))
        id_categoria = int(input('ID da categoria: '))

        repositorio_atualizar_produto(id_produto, nome_produto,descricao, preco, promocao, verificacao_desconto, estoque, id_categoria)

    except ValueError as erro:
        print(f'Ocorreu um erro ao criar produto: {erro}')
        opcao_invalida()
    except Exception as erro:
        print(f'Ocorreu um erro ao deletar produto: {erro}')
        opcao_invalida()

# listar pedidos

# separar pedido
def separar_pedido():
    try:
        print('Pedidos de usuários pendentes: ')
        pedidos_pendentes = usuarios_pedido_pendente()
        if not pedidos_pendentes:
            print('Nenhum pedido está pendente')
            return []
        for pedido in pedidos_pendentes:
            print({
                "id_pedido": pedido[0],
                "nome_usuario": pedido[1],
                "data_pedido": pedido[2].strftime("%d/%m/%Y"),
                "valor_total": pedido[4],
                "status_pedido": pedido[3]
            })
        id_pedido = int(input('Insira o ID do pedido: '))
        modificar_status_pedido(id_pedido, 'pedido separado')
        buscar_pedido(id_pedido)

    except Exception as erro:
        print(f'Ocorreu um erro ao separar pedido: {erro}')
separar_pedido()

def menu_funcionario():
    try:
        while True:
            print(f'{corPadrao}1.{fundoPadrao} Lista de produtos')
            print(f'{corPadrao}2.{fundoPadrao} Adicionar produto')
            print(f'{corPadrao}3.{fundoPadrao} Excluir produto')
            print(f'{corPadrao}4.{fundoPadrao} Atualizar produto')
            print(f'{corPadrao}5.{fundoPadrao} Separar pedido')
            print(f'{corPadrao}6.{fundoPadrao} Ver pedidos')
            print(f'{corPadrao}7.{fundoPadrao} Sair\n')
            opcao_usuario = input("Escolha uma opção: ")
            match opcao_usuario:
                case "1":
                    repositorio_buscar_produtos()
                    voltar_ao_menu_principal()
                case "2":
                    criar_produto()
                case "3":
                    excluir_produto()
                case "4":
                    atualizar_produto()
                case "5":
                    separar_pedido()
                case "6":
                    print("pedidos")
                case "7":
                    print('Saindo...')
                    voltar_ao_menu_principal()
                case _:
                    print("Opção inválida")
    except KeyboardInterrupt:
        print('\nPrograma finalizado com sucesso')