from new_stock import Produto, Estoque, Venda, Relatorio


# ══════════════════════════════════════════════════════════════
#  FUNÇÕES AUXILIARES
# ══════════════════════════════════════════════════════════════

def limpar_tela():
    """Limpa a tela do terminal."""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')


def pausa():
    """Aguarda o usuário pressionar Enter para continuar."""
    input("\n[Pressione ENTER para continuar...]")


def entrada_int(mensagem: str, minimo: int = None, maximo: int = None) -> int:
    """
    Solicita entrada inteira com validação opcional de range.
    
    Parâmetros:
        mensagem: texto a ser exibido
        minimo: valor mínimo aceitável (opcional)
        maximo: valor máximo aceitável (opcional)
    
    Retorno:
        Inteiro validado
    """
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Valor deve ser >= {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Valor deve ser <= {maximo}")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def entrada_float(mensagem: str, minimo: float = None) -> float:
    """
    Solicita entrada decimal com validação opcional.
    
    Parâmetros:
        mensagem: texto a ser exibido
        minimo: valor mínimo aceitável (opcional)
    
    Retorno:
        Float validado
    """
    while True:
        try:
            valor = float(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Valor deve ser >= {minimo}")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número.")


def entrada_texto(mensagem: str) -> str:
    """Solicita entrada de texto não vazia."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Campo obrigatório. Digite algo.")


# ══════════════════════════════════════════════════════════════
#  MENUS - GERENCIAMENTO DE PRODUTOS
# ══════════════════════════════════════════════════════════════

def menu_cadastrar_produto(estoque: Estoque):
    """Menu para cadastrar um novo produto."""
    limpar_tela()
    print("┌─ CADASTRAR NOVO PRODUTO ─────┐")
    
    try:
        nome = entrada_texto("Nome do produto: ")
        codigo = entrada_int("Código (número único): ", minimo=1)
        
        # Verifica se o código já existe
        if codigo in estoque.produtos:
            print("Erro: Já existe um produto com este código.")
            pausa()
            return
        
        categoria = entrada_texto("Categoria: ")
        preco = entrada_float("Preço (R$): ", minimo=0)
        descricao = entrada_texto("Descrição: ")
        fornecedor = entrada_texto("Fornecedor: ")
        quantidade_inicial = entrada_int("Quantidade inicial: ", minimo=0)
        
        # Criar produto e cadastrar no estoque
        produto = Produto(
            nome=nome,
            codigo=codigo,
            categoria=categoria,
            preco=preco,
            descricao=descricao,
            fornecedor=fornecedor
        )
        
        estoque.cadastrar_produto(produto, quantidade_inicial)
        print("Produto cadastrado com sucesso!")
        pausa()
        
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")
        pausa()


def menu_listar_produtos(estoque: Estoque):
    """Menu para listar todos os produtos cadastrados."""
    limpar_tela()
    print("┌─ PRODUTOS CADASTRADOS ─────────┐")
    
    if not estoque.produtos:
        print("Nenhum produto cadastrado.")
    else:
        print(f"\nTotal de produtos: {len(estoque.produtos)}\n")
        for item in estoque.produtos.values():
            produto = item["produto"]
            print(f"  Código: {produto.codigo}")
            print(f"  Nome: {produto.nome}")
            print(f"  Categoria: {produto.categoria}")
            print(f"  Preço: R$ {produto.preco:.2f}")
            print(f"  Fornecedor: {produto.fornecedor}")
            print(f"  Desconto: {produto.desconto_percentual}%")
            print("-" * 40)
    
    pausa()


def menu_aplicar_desconto(estoque: Estoque):
    """Menu para aplicar desconto a um produto."""
    limpar_tela()
    print("┌─ APLICAR DESCONTO A PRODUTO ────┐")
    
    if not estoque.produtos:
        print("Nenhum produto cadastrado.")
        pausa()
        return
    
    try:
        codigo = entrada_int("Código do produto: ")
        
        if codigo not in estoque.produtos:
            print("Produto não encontrado.")
            pausa()
            return
        
        percentual = entrada_float("Percentual de desconto (0-100): ", minimo=0)
        
        if percentual > 100:
            print("Desconto não pode ser maior que 100%")
            pausa()
            return
        
        produto = estoque.produtos[codigo]["produto"]
        produto.aplicar_desconto(percentual)
        print("Desconto aplicado com sucesso!")
        pausa()
        
    except Exception as e:
        print(f"Erro: {e}")
        pausa()


# ══════════════════════════════════════════════════════════════
#  MENUS - GERENCIAMENTO DE ESTOQUE
# ══════════════════════════════════════════════════════════════

def menu_adicionar_estoque(estoque: Estoque):
    """Menu para adicionar quantidade ao estoque de um produto."""
    limpar_tela()
    print("┌─ ADICIONAR ESTOQUE ─────────────┐")
    
    if not estoque.produtos:
        print("Nenhum produto cadastrado.")
        pausa()
        return
    
    try:
        codigo = entrada_int("Código do produto: ")
        quantidade = entrada_int("Quantidade a adicionar: ", minimo=1)
        
        estoque.adicionar_estoque(codigo, quantidade)
        print("Estoque atualizado com sucesso!")
        pausa()
        
    except Exception as e:
        print(f"Erro: {e}")
        pausa()


def menu_remover_estoque(estoque: Estoque):
    """Menu para remover quantidade do estoque de um produto."""
    limpar_tela()
    print("┌─ REMOVER ESTOQUE ───────────────┐")
    
    if not estoque.produtos:
        print("Nenhum produto cadastrado.")
        pausa()
        return
    
    try:
        codigo = entrada_int("Código do produto: ")
        quantidade = entrada_int("Quantidade a remover: ", minimo=1)
        motivo = entrada_texto("Motivo da remoção: ")
        
        estoque.remover_estoque(codigo, quantidade, motivo)
        print("Estoque atualizado com sucesso!")
        pausa()
        
    except Exception as e:
        print(f"Erro: {e}")
        pausa()


def menu_exibir_estoque(estoque: Estoque):
    """Menu para exibir estoque atual."""
    limpar_tela()
    print("┌─ ESTOQUE ATUAL ─────────────────┐\n")
    estoque.exibir_estoque()
    pausa()


def menu_alerta_estoque_baixo(estoque: Estoque):
    """Menu para verificar alertas de estoque baixo."""
    limpar_tela()
    print("┌─ ALERTA DE ESTOQUE BAIXO ───────┐")
    
    limite = entrada_int("Digite o limite de estoque mínimo: ", minimo=1)
    print()
    estoque.alerta_estoque_baixo(limite)
    pausa()


# ══════════════════════════════════════════════════════════════
#  MENUS - VENDAS
# ══════════════════════════════════════════════════════════════

def menu_fazer_venda(estoque: Estoque, relatorio: Relatorio):
    """Menu para realizar uma nova venda."""
    limpar_tela()
    print("┌─ NOVA VENDA ────────────────────┐")
    
    if not estoque.produtos:
        print("Nenhum produto cadastrado. Impossível fazer vendas.")
        pausa()
        return
    
    try:
        # ── Inicializa a venda ──────────────────────────────────────
        nome_cliente = entrada_texto("Nome do cliente: ")
        venda = Venda(estoque, cliente=nome_cliente)
        
        # ── Adiciona itens à venda ──────────────────────────────────
        while True:
            print("\n[ADICIONAR ITENS À VENDA]")
            codigo = entrada_int("Código do produto (0 para finalizar): ")
            
            if codigo == 0:
                break
            
            if codigo not in estoque.produtos:
                print("Produto não encontrado.")
                continue
            
            quantidade = entrada_int("Quantidade: ", minimo=1)
            venda.adicionar_item(codigo, quantidade)
        
        # ── Aplica desconto global (opcional) ────────────────────────
        if venda.itens:
            aplicar_desconto = entrada_texto("\nDeseja aplicar desconto global? (s/n): ").lower()
            
            if aplicar_desconto == 's':
                desconto = entrada_float("Percentual de desconto (0-100): ", minimo=0)
                venda.aplicar_desconto_global(desconto)
        
        # ── Finaliza a venda ────────────────────────────────────────
        if venda.itens:
            print("\n" + "=" * 45)
            dados = venda.finalizar_venda()
            
            if dados:
                venda.emitir_recibo()
                relatorio.registrar_venda(dados)
                print("Venda registrada no relatório!")
        else:
            print("Nenhum item foi adicionado à venda.")
        
        pausa()
        
    except Exception as e:
        print(f"Erro ao processar venda: {e}")
        pausa()


# ══════════════════════════════════════════════════════════════
#  MENUS - RELATÓRIOS
# ══════════════════════════════════════════════════════════════

def menu_relatorio_vendas(relatorio: Relatorio):
    """Menu para exibir relatório de vendas."""
    limpar_tela()
    print("┌─ RELATÓRIO DE VENDAS ───────────┐\n")
    relatorio.relatorio_vendas()
    pausa()


def menu_relatorio_estoque(relatorio: Relatorio):
    """Menu para exibir relatório de estoque."""
    limpar_tela()
    print("┌─ RELATÓRIO DE ESTOQUE ──────────┐\n")
    relatorio.relatorio_estoque()
    pausa()


def menu_historico_movimentacoes(relatorio: Relatorio):
    """Menu para exibir histórico de movimentações."""
    limpar_tela()
    print("┌─ HISTÓRICO DE MOVIMENTAÇÕES ────┐\n")
    relatorio.historico_movimentacoes()
    pausa()


# ══════════════════════════════════════════════════════════════
#  MENUS - PERSISTÊNCIA
# ══════════════════════════════════════════════════════════════

def menu_salvar_dados(estoque: Estoque, relatorio: Relatorio):
    """Menu para salvar dados do estoque e relatórios."""
    limpar_tela()
    print("┌─ SALVAR DADOS ──────────────────┐\n")
    
    try:
        arquivo_estoque = entrada_texto("Nome do arquivo estoque [estoque.json]: ").strip() or "estoque.json"
        arquivo_relatorio = entrada_texto("Nome do arquivo relatório [relatorio_vendas.json]: ").strip() or "relatorio_vendas.json"
        
        estoque.salvar(arquivo_estoque)
        relatorio.salvar_relatorio(arquivo_relatorio)
        print("Dados salvos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    
    pausa()


def menu_carregar_dados(estoque: Estoque, relatorio: Relatorio):
    """Menu para carregar dados do estoque e relatórios."""
    limpar_tela()
    print("┌─ CARREGRAR DADOS ───────────────┐\n")
    
    try:
        arquivo_estoque = entrada_texto("Nome do arquivo estoque [estoque.json]: ").strip() or "estoque.json"
        arquivo_relatorio = entrada_texto("Nome do arquivo relatório [relatorio_vendas.json]: ").strip() or "relatorio_vendas.json"
        
        estoque.carregar(arquivo_estoque)
        relatorio.carregar_relatorio(arquivo_relatorio)
        print("Dados carregados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao carregar: {e}")
    
    pausa()


# ══════════════════════════════════════════════════════════════
#  MENUS PRINCIPAIS
# ══════════════════════════════════════════════════════════════

def menu_produtos(estoque: Estoque):
    """Submenu de gerenciamento de produtos."""
    while True:
        limpar_tela()
        print("""
╔═══════════════════════════════════════╗
║   GERENCIAMENTO DE PRODUTOS           ║
╚═══════════════════════════════════════╝

1. Cadastrar novo produto
2. Listar produtos
3. Aplicar desconto a um produto
4. Voltar ao menu principal

""")
        
        opcao = entrada_texto("Escolha uma opção (1-4): ")
        
        if opcao == '1':
            menu_cadastrar_produto(estoque)
        elif opcao == '2':
            menu_listar_produtos(estoque)
        elif opcao == '3':
            menu_aplicar_desconto(estoque)
        elif opcao == '4':
            break
        else:
            print("Opção inválida.")
            pausa()


def menu_estoque_submenu(estoque: Estoque):
    """Submenu de gerenciamento de estoque."""
    while True:
        limpar_tela()
        print("""
╔═══════════════════════════════════════╗
║   GERENCIAMENTO DE ESTOQUE            ║
╚═══════════════════════════════════════╝

1. Exibir estoque atual
2. Adicionar quantidade ao estoque
3. Remover quantidade do estoque
4. Verificar estoque baixo
5. Voltar ao menu principal

""")
        
        opcao = entrada_texto("Escolha uma opção (1-5): ")
        
        if opcao == '1':
            menu_exibir_estoque(estoque)
        elif opcao == '2':
            menu_adicionar_estoque(estoque)
        elif opcao == '3':
            menu_remover_estoque(estoque)
        elif opcao == '4':
            menu_alerta_estoque_baixo(estoque)
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")
            pausa()


def menu_relatorios(relatorio: Relatorio):
    """Submenu de relatórios."""
    while True:
        limpar_tela()
        print("""
╔═══════════════════════════════════════╗
║   RELATÓRIOS                          ║
╚═══════════════════════════════════════╝

1. Relatório de vendas
2. Relatório de estoque
3. Histórico de movimentações
4. Voltar ao menu principal

""")
        
        opcao = entrada_texto("Escolha uma opção (1-4): ")
        
        if opcao == '1':
            menu_relatorio_vendas(relatorio)
        elif opcao == '2':
            menu_relatorio_estoque(relatorio)
        elif opcao == '3':
            menu_historico_movimentacoes(relatorio)
        elif opcao == '4':
            break
        else:
            print("Opção inválida.")
            pausa()


def menu_principal():
    """Menu principal do sistema."""
    
    # ── Inicializa as instâncias principais ──────────────────────────
    estoque = Estoque()
    relatorio = Relatorio(estoque)
    
    # Tenta carregar dados anteriores automaticamente
    print("Carregando dados...")
    estoque.carregar()
    relatorio.carregar_relatorio()
    print("Pronto!\n")
    
    while True:
        limpar_tela()
        print("""
╔═══════════════════════════════════════╗
║   SISTEMA DE GERENCIAMENTO DE ESTOQUE ║
╚═══════════════════════════════════════╝

1. Gerenciar produtos
2. Gerenciar estoque
3. Realizar venda
4. Relatórios
5. Salvar dados
6. Carregar dados
7. Sair

""")
        
        opcao = entrada_texto("Escolha uma opção (1-7): ")
        
        if opcao == '1':
            menu_produtos(estoque)
        elif opcao == '2':
            menu_estoque_submenu(estoque)
        elif opcao == '3':
            menu_fazer_venda(estoque, relatorio)
        elif opcao == '4':
            menu_relatorios(relatorio)
        elif opcao == '5':
            menu_salvar_dados(estoque, relatorio)
        elif opcao == '6':
            menu_carregar_dados(estoque, relatorio)
        elif opcao == '7':
            print("\nAté logo!\n")
            break
        else:
            print("Opção inválida.")
            pausa()


# ══════════════════════════════════════════════════════════════
#  PONTO DE ENTRADA DO PROGRAMA
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    menu_principal()
