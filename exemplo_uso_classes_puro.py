from new_stock import Produto, Estoque, Venda, Relatorio

estoque = Estoque()
relatorio = Relatorio(estoque)


produto_caderno = Produto(
    nome="Caderno Universitario",
    codigo=1001,
    categoria="Papelaria",
    preco=24.90,
    descricao="Caderno espiral com 200 folhas",
    fornecedor="Fornecedor Escolar"
)

produto_caneta = Produto(
    nome="Caneta Azul",
    codigo=1002,
    categoria="Papelaria",
    preco=3.50,
    descricao="Caneta esferografica azul",
    fornecedor="Fornecedor Escrita"
)

produto_mochila = Produto(
    nome="Mochila Executiva",
    codigo=1003,
    categoria="Acessorios",
    preco=159.90,
    descricao="Mochila preta com compartimento para notebook",
    fornecedor="Fornecedor Bolsas"
)



produto_caneta.aplicar_desconto(10) # let's use everything at the last drop


# estoque.cadastrar_produto(produto_caderno, quantidade_inicial=20)
# estoque.cadastrar_produto(produto_caneta, quantidade_inicial=100)
# estoque.cadastrar_produto(produto_mochila, quantidade_inicial=8)



# estoque.exibir_estoque()
# estoque.alerta_estoque_baixo(limite=10)


# estoque.adicionar_estoque(codigo=1001, quantidade=5)
# estoque.remover_estoque(codigo=1002, quantidade=3, motivo="ODEIO O CANETA AZUL")
# estoque.atualizar_estoque(codigo=1003, nova_quantidade=10)



# estoque.exibir_estoque()
# estoque.alerta_estoque_baixo(limite=10)



# venda = Venda(estoque, cliente="Maria Souza")
# venda.adicionar_item(codigo=1001, quantidade=2)
# venda.adicionar_item(codigo=1002, quantidade=5)
# venda.aplicar_desconto_global(5)

# dados_venda = venda.finalizar_venda()
# venda.emitir_recibo()


# relatorio.registrar_venda(dados_venda)

# relatorio.relatorio_vendas()
# relatorio.relatorio_estoque()
# relatorio.historico_movimentacoes()




# print(f"Produtos criados: {Produto.contar_produtos()}")
# print(f"Estoques criados: {Estoque.contar_estoque()}")
# print(f"Vendas criadas: {Venda.contar_vendas()}")


# estoque.salvar("demo_estoque.json")
# relatorio.salvar_relatorio("demo_relatorio_vendas.json")