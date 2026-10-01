import json
from utils import voltar_ao_menu_principal

fundoPadrao = '\033[0;0m'
corNumerosPadrao = '\033[1;35m'

ARQUIVO = "produtos.json"

def salvar_produto_no_arquivo():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)

def carregar_produto():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

produtos = carregar_produto()

def adicionar_produto():
    print('Adicione um produto:')
    novo_produto = input('Nome do produto: ')
    preco = float(input('Preço do produto: '))
    descricao = input('Descrição do produto: ')
    promocao = input('O produto está com desconto? (s/n): ').lower().startswith('s')
    verificacaoDesconto = lambda promocao: float(input('Desconto do produto (em porcentagem): ')) if promocao == True else 0

    novo_produto = {
        "id": len(produtos) + 1,
        "nome": novo_produto,
        "descricao": descricao,
        "preco": preco,
        "promocao": promocao,
        "valorPromocao": verificacaoDesconto(promocao)
    }

    produtos.append(novo_produto)
    salvar_produto_no_arquivo()
    print("Produto salvo!")

    print(f'Lista de produtos: \n')
    for i, produto in enumerate(produtos, start=1):
        print(f"{i}. {produto['nome']}")

def lista_de_produtos():
    print('Lista de produtos: \n')

    if not produtos:
        print('Ainda não tem nenhum produto, crie um: ')
        adicionar_produto()
    else:
        for indice, produto in enumerate(produtos, start=1):
            print(f"{indice} - {produto['nome']}")

def excluir_produto():
    print(lista_de_produtos())
    produto_excluido_id = int(input('Digite o número do id do produto a ser excluído: '))

    try:
        indice = produto_excluido_id - 1
        if 0 <= indice < len(produtos):
            produto_excluido = produtos.pop(indice)
            salvar_produto_no_arquivo(produtos)
            print(f"Tarefa '{produto_excluido['titulo']}' removida!")

        print(lista_de_produtos())
    except ValueError:
        print(f'\033[1;33mDigite um número válido\033[0;0m')


def atualizar_campo(mensagem, valor_antigo):
    novo_valor = input(f"{mensagem} (atual: {valor_antigo}): ").strip()
    print(f'valor antigo: {valor_antigo}')

    if not novo_valor:
        return valor_antigo
    tipo_original = type(valor_antigo)
    print(f"tipo: {tipo_original}")

    try:
        return tipo_original(novo_valor)
    except ValueError:
        print(f"Formato inválido! O valor deveria ser um {tipo_original.__name__}.")
        print("A alteração foi cancelada e o valor antigo foi mantido.")
        return valor_antigo

# promocao = False
# nova_promocao = atualizar_campo("Digite o novo valor da promoção: ", 5)
# if nova_promocao > 0:
#     promocao = True
# print(nova_promocao)
# print(promocao)

def atualizar_produto():
    lista_de_produtos()
    id_produto = int(input('Digite o ID do produto: '))
    produto = None
    for indice, produto in enumerate(produtos):
        if produto['id'] == id_produto:
            try:
                novo_nome = produto['nome']
                nova_descricao = produto['descricao']
                novo_preco = produto['preco']
                nova_promocao = produto['valorPromocao']
                if isinstance(nova_promocao, bool):
                    nova_promocao = 0
                promocao = produto['promocao']
                while True:
                    print(f"Produto que vai ser atualizado: {produto['nome']}")
                    print(f'{corNumerosPadrao}1.{fundoPadrao} Atualizar nome')
                    print(f'{corNumerosPadrao}2.{fundoPadrao} Atualizar descrição')
                    print(f'{corNumerosPadrao}3.{fundoPadrao} Atualizar o preço')
                    print(f'{corNumerosPadrao}4.{fundoPadrao} Atualizar o valor da promoção')
                    print(f'{corNumerosPadrao}5.{fundoPadrao} Finalizar atualização')
                    print(f'{corNumerosPadrao}6.{fundoPadrao} Cancelar')

                    escolha_menu = input("Escolha um dos itens para atualizar o produto: ")
                    match escolha_menu:
                        case "1":
                            novo_nome = atualizar_campo("Digite o novo nome do produto: ", produto['nome'])
                        case "2":
                            nova_descricao = atualizar_campo("Digite a nova descrição: ", produto['descricao'])
                        case "3":
                            novo_preco = atualizar_campo("Digite o novo preço do produto: ", produto['preco'])
                        case "4":
                            nova_promocao = atualizar_campo("Digite o novo valor da promoção: ", nova_promocao)
                            promocao = nova_promocao > 0
                        case "5":
                            produto_atualizado = {
                                "id": id_produto,
                                "nome": novo_nome,
                                "descricao": nova_descricao,
                                "preco": novo_preco,
                                "promocao": promocao,
                                "valorPromocao": nova_promocao
                            }

                            produtos[indice] = produto_atualizado
                            salvar_produto_no_arquivo()
                            print("Produto atualizado com sucesso!")
                            voltar_ao_menu_principal()
                        case "6":
                            print("Cancelando...")
                            voltar_ao_menu_principal()
                        case _:
                            print('Opção inválida')
            except KeyboardInterrupt:
                print('\nPrograma finalizado com sucesso')