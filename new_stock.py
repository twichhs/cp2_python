from datetime import datetime   # usado para registrar data/hora das operações
import json                    # usado para salvar/carregar dados em JSON
import os                      # usado para verificar existência de arquivos

# ══════════════════════════════════════════════════════════════
#  CLASSE PRODUTO
#  Representa um produto com suas informações básicas.
# ══════════════════════════════════════════════════════════════
class Produto:

    # Variável de classe: conta quantos produtos já foram criados
    contador_produtos = 0

    def __init__(
        self,
        nome: str,
        codigo: int,
        categoria: str,
        preco: float,
        descricao: str,
        fornecedor: str
    ):
        """
        Inicializa um produto validando todos os campos obrigatórios.

        Parâmetros:
            nome       : nome do produto (ex: 'Caneta Azul')
            codigo     : identificador único inteiro (ex: 1001)
            categoria  : categoria do produto (ex: 'Papelaria')
            preco      : preço unitário em reais (deve ser >= 0)
            descricao  : descrição livre do produto
            fornecedor : nome do fornecedor
        """
        try:
            # ── Validações dos campos ──────────────────────────────
            if not isinstance(nome, str) or nome.strip() == "":
                raise ValueError("Nome inválido")

            if not isinstance(codigo, int):
                raise ValueError("Código deve ser inteiro")

            if not isinstance(categoria, str) or categoria.strip() == "":
                raise ValueError("Categoria inválida")

            if preco < 0:
                raise ValueError("Preço não pode ser negativo")

            if not isinstance(fornecedor, str) or fornecedor.strip() == "":
                raise ValueError("Fornecedor inválido")

            # ── Atribuição dos atributos ───────────────────────────
            self.nome       = nome
            self.codigo     = codigo
            self.categoria  = categoria
            self.preco      = preco           # preço original sem desconto
            self.descricao  = descricao
            self.fornecedor = fornecedor

            # Desconto padrão começa em 0 % pode ser alterado depois
            self.desconto_percentual: float = 0.0

            # Incrementa o contador global de produtos criados
            Produto.contador_produtos += 1

        except ValueError as e:
            print(f"Erro ao criar produto: {e}")
            raise

    # ── Propriedade calculada: preço já com desconto aplicado ──────
    @property
    def preco_com_desconto(self) -> float:
        """Retorna o preço unitário após aplicar o desconto percentual."""
        return self.preco * (1 - self.desconto_percentual / 100)

    def aplicar_desconto(self, percentual: float):
        """
        Define o desconto do produto em %.
        Ex: aplicar_desconto(10) → 10 % de desconto.

        Parâmetros:
            percentual: valor entre 0 e 100
        """
        if not (0 <= percentual <= 100):
            raise ValueError("Percentual de desconto deve estar entre 0 e 100")
        self.desconto_percentual = percentual
        print(f"Desconto de {percentual}% aplicado em '{self.nome}'.")

    def info(self):
        """Exibe as informações completas do produto no terminal."""
        print(
            f"\n── Produto ──────────────────\n"
            f"  Nome      : {self.nome}\n"
            f"  Código    : {self.codigo}\n"
            f"  Categoria : {self.categoria}\n"
            f"  Preço     : R$ {self.preco:.2f}\n"
            f"  Desconto  : {self.desconto_percentual}%\n"
            f"  Preço c/desc: R$ {self.preco_com_desconto:.2f}\n"
            f"  Descrição : {self.descricao}\n"
            f"  Fornecedor: {self.fornecedor}"
        )

    @classmethod
    def contar_produtos(cls) -> int:
        """Retorna o total de instâncias de Produto criadas."""
        return cls.contador_produtos


# ══════════════════════════════════════════════════════════════
#  CLASSE ESTOQUE
#  Gerencia o inventário: cadastro, adição, remoção e alertas.
# ══════════════════════════════════════════════════════════════
class Estoque:

    # Variável de classe: conta quantos estoques foram criados
    contador_estoques = 0

    def __init__(self):
        """
        Inicializa um estoque vazio.

        Estrutura interna de self.produtos:
            {
              codigo_int: {
                "produto"   : objeto Produto,
                "quantidade": int
              },
              ...
            }
        """
        # Dicionário principal que armazena todos os itens do estoque
        self.produtos: dict = {}

        # Histórico de movimentações: lista de dicionários com detalhes
        # de cada adição ou remoção ocorrida neste estoque
        self.historico_movimentacoes: list[dict] = []

        Estoque.contador_estoques += 1

    # ── Consulta ────────────────────────────────────────────────────

    def exibir_estoque(self):
        """Exibe todos os produtos e suas quantidades no terminal."""
        try:
            if not self.produtos:
                print("O estoque está vazio.")
                return

            print("\n" + "=" * 40)
            print("           ESTOQUE ATUAL")
            print("=" * 40)

            for item in self.produtos.values():
                produto   = item["produto"]
                quantidade = item["quantidade"]

                print(f"  Nome      : {produto.nome}")
                print(f"  Código    : {produto.codigo}")
                print(f"  Categoria : {produto.categoria}")
                print(f"  Quantidade: {quantidade}")
                print(f"  Preço     : R$ {produto.preco:.2f}")
                print(f"  Fornecedor: {produto.fornecedor}")
                print("-" * 40)

        except Exception as e:
            print(f"Erro ao exibir estoque: {e}")

    # ── Cadastro ────────────────────────────────────────────────────

    def cadastrar_produto(self, produto: "Produto", quantidade_inicial: int = 0):
        """
        Adiciona um produto ao estoque pela primeira vez.

        Parâmetros:
            produto           : instância de Produto
            quantidade_inicial: estoque inicial (padrão 0)
        """
        try:
            if produto.codigo in self.produtos:
                raise ValueError("Já existe um produto com esse código")

            if quantidade_inicial < 0:
                raise ValueError("Quantidade inicial não pode ser negativa")

            # Registra o produto no dicionário principal
            self.produtos[produto.codigo] = {
                "produto"   : produto,
                "quantidade": quantidade_inicial
            }

            # Salva a movimentação de entrada inicial no histórico
            if quantidade_inicial > 0:
                self._registrar_movimentacao(
                    tipo="entrada",
                    codigo=produto.codigo,
                    nome=produto.nome,
                    quantidade=quantidade_inicial,
                    motivo="cadastro inicial"
                )

            print(f"Produto '{produto.nome}' cadastrado com sucesso.")

        except (ValueError, KeyError) as e:
            print(f"Erro ao cadastrar produto: {e}")

    # ── Movimentações ────────────────────────────────────────────────

    def adicionar_estoque(self, codigo: int, quantidade: int):
        """
        Aumenta a quantidade de um produto já cadastrado.

        Parâmetros:
            codigo    : código do produto
            quantidade: quantidade a adicionar (deve ser > 0)
        """
        try:
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser positiva")

            if codigo not in self.produtos:
                raise KeyError("Produto não encontrado no estoque")

            self.produtos[codigo]["quantidade"] += quantidade

            # Registra a entrada no histórico de movimentações
            nome = self.produtos[codigo]["produto"].nome
            self._registrar_movimentacao("entrada", codigo, nome, quantidade, "reposição")

            print(f"Estoque de '{nome}' atualizado. Nova quantidade: {self.produtos[codigo]['quantidade']}")

        except (ValueError, KeyError) as e:
            print(f"Erro ao adicionar estoque: {e}")

    def remover_estoque(self, codigo: int, quantidade: int, motivo: str = "remoção manual"):
        """
        Reduz a quantidade de um produto no estoque.

        Parâmetros:
            codigo    : código do produto
            quantidade: quantidade a remover (deve ser > 0)
            motivo    : descrição do motivo (padrão: 'remoção manual')
        """
        try:
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser positiva")

            if codigo not in self.produtos:
                raise KeyError("Produto não encontrado no estoque")

            item = self.produtos[codigo]

            if item["quantidade"] < quantidade:
                raise ValueError(
                    f"Estoque insuficiente. Disponível: {item['quantidade']}, "
                    f"Solicitado: {quantidade}"
                )

            item["quantidade"] -= quantidade

            # Registra a saída no histórico de movimentações
            self._registrar_movimentacao("saída", codigo, item["produto"].nome, quantidade, motivo)

            print(f"Produto removido. Estoque restante de '{item['produto'].nome}': {item['quantidade']}")

        except (ValueError, KeyError) as e:
            print(f"Erro ao remover estoque: {e}")

    def atualizar_estoque(self, codigo: int, nova_quantidade: int):
        """
        Define uma quantidade absoluta para um produto, sobrescrevendo a atual.

        Parâmetros:
            codigo         : código do produto
            nova_quantidade: novo valor de estoque (>= 0)
        """
        try:
            if nova_quantidade < 0:
                raise ValueError("Quantidade não pode ser negativa")

            if codigo not in self.produtos:
                raise KeyError("Produto não encontrado no estoque")

            quantidade_anterior = self.produtos[codigo]["quantidade"]
            self.produtos[codigo]["quantidade"] = nova_quantidade

            # Determina se foi entrada ou saída para registrar corretamente
            diferenca = nova_quantidade - quantidade_anterior
            if diferenca != 0:
                tipo   = "entrada" if diferenca > 0 else "saída"
                nome   = self.produtos[codigo]["produto"].nome
                self._registrar_movimentacao(tipo, codigo, nome, abs(diferenca), "ajuste manual")

            print(f"Quantidade atualizada para {nova_quantidade}.")

        except (ValueError, KeyError) as e:
            print(f"Erro ao atualizar estoque: {e}")

    # ── Alertas ─────────────────────────────────────────────────────

    def alerta_estoque_baixo(self, limite: int):
        """
        Exibe produtos cujo estoque está abaixo ou igual ao limite informado.

        Parâmetros:
            limite: quantidade mínima aceitável
        """
        try:
            produtos_baixos = [
                item for item in self.produtos.values()
                if item["quantidade"] <= limite
            ]

            if not produtos_baixos:
                print(f"Nenhum produto com estoque abaixo ou igual a {limite}.")
                return

            print(f"\n⚠  ALERTA — Estoque baixo (limite: {limite})")
            print("-" * 40)
            for item in produtos_baixos:
                print(f"  {item['produto'].nome} → {item['quantidade']} unidades")

        except Exception as e:
            print(f"Erro no alerta de estoque: {e}")

    # ── Método auxiliar interno ──────────────────────────────────────

    def _registrar_movimentacao(
        self,
        tipo: str,
        codigo: int,
        nome: str,
        quantidade: int,
        motivo: str
    ):
        """
        Método privado: salva um registro no histórico de movimentações.
        Não deve ser chamado diretamente fora da classe.

        Parâmetros:
            tipo      : 'entrada' ou 'saída'
            codigo    : código do produto
            nome      : nome do produto
            quantidade: unidades movimentadas
            motivo    : texto explicativo da operação
        """
        self.historico_movimentacoes.append({
            "data_hora" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo"      : tipo,
            "codigo"    : codigo,
            "nome"      : nome,
            "quantidade": quantidade,
            "motivo"    : motivo
        })

    @classmethod
    def contar_estoque(cls) -> int:
        """Retorna o número total de instâncias de Estoque criadas."""
        return cls.contador_estoques

    # ── Persistência de dados ───────────────────────────────────────

    def salvar(self, arquivo: str = "estoque.json"):
        """
        Salva o estoque (produtos e histórico) em arquivo JSON.

        Parâmetros:
            arquivo: caminho do arquivo JSON (padrão: 'estoque.json')
        """
        try:
            dados = {
                "produtos": {},
                "historico_movimentacoes": self.historico_movimentacoes
            }

            # Converte produtos para formato serializável
            for codigo, item in self.produtos.items():
                produto = item["produto"]
                dados["produtos"][str(codigo)] = {
                    "nome": produto.nome,
                    "codigo": produto.codigo,
                    "categoria": produto.categoria,
                    "preco": produto.preco,
                    "descricao": produto.descricao,
                    "fornecedor": produto.fornecedor,
                    "desconto_percentual": produto.desconto_percentual,
                    "quantidade": item["quantidade"]
                }

            # Salva em JSON
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)

            print(f"✅ Estoque salvo com sucesso em '{arquivo}'.")

        except (IOError, OSError) as e:
            print(f"Erro ao salvar estoque: {e}")

    def carregar(self, arquivo: str = "estoque.json") -> bool:
        """
        Carrega o estoque (produtos e histórico) a partir de arquivo JSON.
        Limpa o estoque atual antes de carregar.

        Parâmetros:
            arquivo: caminho do arquivo JSON (padrão: 'estoque.json')

        Retorno:
            True se carregou com sucesso, False caso contrário
        """
        try:
            if not os.path.exists(arquivo):
                print(f"Arquivo '{arquivo}' não encontrado. Estoque iniciado vazio.")
                return False

            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Limpa o estoque atual
            self.produtos.clear()
            self.historico_movimentacoes.clear()

            # Reconstrói os produtos
            for codigo_str, prod_dados in dados.get("produtos", {}).items():
                produto = Produto(
                    nome=prod_dados["nome"],
                    codigo=prod_dados["codigo"],
                    categoria=prod_dados["categoria"],
                    preco=prod_dados["preco"],
                    descricao=prod_dados["descricao"],
                    fornecedor=prod_dados["fornecedor"]
                )
                produto.desconto_percentual = prod_dados["desconto_percentual"]

                self.produtos[produto.codigo] = {
                    "produto": produto,
                    "quantidade": prod_dados["quantidade"]
                }

            # Reconstrói o histórico
            self.historico_movimentacoes = dados.get("historico_movimentacoes", [])

            print(f"✅ Estoque carregado com sucesso de '{arquivo}'.")
            return True

        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON em '{arquivo}'. Arquivo corrompido?")
            return False
        except (IOError, OSError) as e:
            print(f"Erro ao carregar estoque: {e}")
            return False


# ══════════════════════════════════════════════════════════════
#  CLASSE VENDA
#  Registra vendas, atualiza o estoque automaticamente
#  e emite recibos com suporte a descontos por item ou globais.
# ══════════════════════════════════════════════════════════════
class Venda:

    contador_vendas = 0

    def __init__(self, estoque: Estoque, cliente: str = "Cliente"):
        """
        Inicializa uma nova venda vinculada a um estoque.

        Parâmetros:
            estoque: instância de Estoque de onde os produtos serão retirados
            cliente: nome do cliente (opcional, padrão 'Cliente')
        """
        # estoque será atualizado automaticamente
        self.estoque  = estoque


        self.cliente  = cliente

        # { "produto": Produto, "quantidade": int, "preco_unitario": float }
        self.itens: list[dict] = []

        # Data e hora do registro da venda
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Número único da venda
        Venda.contador_vendas += 1
        self.numero_venda = Venda.contador_vendas

        # Desconto global aplicado ao valor total da venda (em %)
        self.desconto_global: float = 0.0

    # ── Adição de itens ─────────────────────────────────────────────

    def adicionar_item(self, codigo: int, quantidade: int):
        """
        Adiciona um produto à venda verificando disponibilidade em estoque.
        O preço capturado é o preço COM desconto do produto no momento da venda.

        Parâmetros:
            codigo    : código do produto no estoque
            quantidade: quantidade desejada (deve ser > 0)
        """
        try:
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser positiva")

            # Verifica se o produto existe no estoque
            if codigo not in self.estoque.produtos:
                raise KeyError(f"Produto com código {codigo} não encontrado no estoque")

            item_estoque = self.estoque.produtos[codigo]

            # Verifica se há estoque suficiente
            if item_estoque["quantidade"] < quantidade:
                raise ValueError(
                    f"Estoque insuficiente para '{item_estoque['produto'].nome}'. "
                    f"Disponível: {item_estoque['quantidade']}, Solicitado: {quantidade}"
                )

            produto = item_estoque["produto"]

            # Captura o preço com desconto do produto no momento da venda
            preco_unitario = produto.preco_com_desconto

            # Registra o item na lista da venda
            self.itens.append({
                "produto"       : produto,
                "quantidade"    : quantidade,
                "preco_unitario": preco_unitario   # preço já com desconto do produto
            })

            print(f"  ✔ '{produto.nome}' × {quantidade} adicionado(s) à venda.")

        except (ValueError, KeyError) as e:
            print(f"Erro ao adicionar item: {e}")

    # ── Descontos ────────────────────────────────────────────────────

    def aplicar_desconto_global(self, percentual: float):
        """
        Aplica um desconto percentual sobre o VALOR TOTAL da venda.
        Útil para promoções por volume ou cupons de desconto.

        Parâmetros:
            percentual: valor entre 0 e 100
        """
        if not (0 <= percentual <= 100):
            raise ValueError("Percentual deve estar entre 0 e 100")
        self.desconto_global = percentual
        print(f"Desconto global de {percentual}% aplicado na venda #{self.numero_venda}.")

    # ── Cálculos internos ────────────────────────────────────────────

    def _calcular_subtotal(self) -> float:
        """
        Calcula o subtotal da venda (soma de preço × quantidade de cada item),
        antes do desconto global.
        """
        return sum(
            item["preco_unitario"] * item["quantidade"]
            for item in self.itens
        )

    def _calcular_total(self) -> float:
        """
        Calcula o valor final da venda aplicando o desconto global ao subtotal.
        """
        subtotal = self._calcular_subtotal()
        return subtotal * (1 - self.desconto_global / 100)

    # ── Finalização da venda ─────────────────────────────────────────

    def finalizar_venda(self) -> dict | None:
        """
        Finaliza a venda:
          1. Valida que há itens no carrinho.
          2. Debita automaticamente cada item do estoque.
          3. Retorna o dicionário com os dados completos da venda
             (usado por Relatorio para registrar no histórico).

        Retorno:
            Dicionário com dados da venda ou None se houver erro.
        """
        try:
            if not self.itens:
                raise ValueError("Não é possível finalizar uma venda sem itens")

            # ── Atualização automática do estoque ──────────────────
            for item in self.itens:
                self.estoque.remover_estoque(
                    codigo    = item["produto"].codigo,
                    quantidade= item["quantidade"],
                    motivo    = f"venda #{self.numero_venda}"  # rastreia a origem
                )

            # ── Monta o dicionário de resultado da venda ───────────
            dados_venda = {
                "numero_venda"    : self.numero_venda,
                "data_hora"       : self.data_hora,
                "cliente"         : self.cliente,
                "itens"           : self.itens,
                "subtotal"        : self._calcular_subtotal(),
                "desconto_global" : self.desconto_global,
                "total"           : self._calcular_total()
            }

            print(f"\n✅ Venda #{self.numero_venda} finalizada com sucesso!")
            return dados_venda

        except (ValueError, KeyError) as e:
            print(f"Erro ao finalizar venda: {e}")
            return None

    # ── Recibo ───────────────────────────────────────────────────────

    def emitir_recibo(self):
        """
        Exibe um recibo formatado da venda no terminal.
        Deve ser chamado APÓS finalizar_venda() para garantir
        que os valores são definitivos.
        """
        if not self.itens:
            print("Nenhum item na venda. Adicione produtos antes de emitir o recibo.")
            return

        subtotal = self._calcular_subtotal()
        total    = self._calcular_total()
        economia = subtotal - total   # quanto o cliente economizou com desconto global

        print("\n" + "=" * 45)
        print("           RECIBO DE VENDA")
        print("=" * 45)
        print(f"  Venda Nº  : {self.numero_venda}")
        print(f"  Data/Hora : {self.data_hora}")
        print(f"  Cliente   : {self.cliente}")
        print("-" * 45)
        print(f"  {'PRODUTO':<20} {'QTD':>5} {'UNIT':>8} {'TOTAL':>9}")
        print("-" * 45)

        # Linha de cada produto vendido
        for item in self.itens:
            nome   = item["produto"].nome[:20]   # limita o nome a 20 chars na exibição
            qtd    = item["quantidade"]
            unit   = item["preco_unitario"]
            total_item = unit * qtd
            print(f"  {nome:<20} {qtd:>5} {unit:>8.2f} {total_item:>9.2f}")

        print("-" * 45)
        print(f"  {'Subtotal':<35} R$ {subtotal:>7.2f}")

        # Exibe desconto global apenas se houver
        if self.desconto_global > 0:
            print(f"  {'Desconto (' + str(self.desconto_global) + '%)':<35} R$ {economia:>7.2f}")

        print(f"  {'TOTAL A PAGAR':<35} R$ {total:>7.2f}")
        print("=" * 45)
        print("     Obrigado pela preferência! 🛒")
        print("=" * 45 + "\n")

    @classmethod
    def contar_vendas(cls) -> int:
        """Retorna o total de vendas registradas."""
        return cls.contador_vendas


# ══════════════════════════════════════════════════════════════
#  CLASSE RELATORIO
#  Gera relatórios de vendas, estoque e histórico de movimentações.
# ══════════════════════════════════════════════════════════════
class Relatorio:

    def __init__(self, estoque: Estoque):
        """
        Inicializa o sistema de relatórios vinculado a um estoque.

        Parâmetros:
            estoque: instância de Estoque a ser consultada nos relatórios
        """
        # Estoque monitorado por este relatório
        self.estoque = estoque

        # Registro interno de todas as vendas finalizadas
        # Cada entrada é o dicionário retornado por Venda.finalizar_venda()
        self.vendas_registradas: list[dict] = []

    # ── Registro de vendas ───────────────────────────────────────────

    def registrar_venda(self, dados_venda: dict):
        """
        Salva os dados de uma venda finalizada no histórico de relatórios.
        Deve ser chamado logo após Venda.finalizar_venda().

        Parâmetros:
            dados_venda: dicionário retornado por Venda.finalizar_venda()
        """
        if dados_venda is None:
            print("Venda inválida. Nenhum dado registrado no relatório.")
            return

        self.vendas_registradas.append(dados_venda)
        print(f"Venda #{dados_venda['numero_venda']} registrada no relatório.")

    # ── Relatório de vendas ──────────────────────────────────────────

    def relatorio_vendas(self):
        """
        Exibe o relatório detalhado de todas as vendas registradas,
        incluindo: número, data, cliente, produtos, quantidades e totais.
        """
        if not self.vendas_registradas:
            print("Nenhuma venda registrada ainda.")
            return

        print("\n" + "=" * 50)
        print("          RELATÓRIO DE VENDAS")
        print("=" * 50)

        total_geral = 0.0   # acumulador para o total de todas as vendas

        for venda in self.vendas_registradas:
            print(f"\n  Venda Nº  : {venda['numero_venda']}")
            print(f"  Data/Hora : {venda['data_hora']}")
            print(f"  Cliente   : {venda['cliente']}")
            print(f"  {'PRODUTO':<22} {'QTD':>5} {'UNIT':>8} {'SUBTOTAL':>10}")
            print("  " + "-" * 48)

            # Detalha cada item da venda
            for item in venda["itens"]:
                # Suporta tanto dados completos (com objetos) quanto dados carregados do JSON
                if "produto_nome" in item:  # Carregado do JSON (dados simplificados)
                    nome  = item["produto_nome"][:22]
                else:  # Dados completos (com objeto Produto)
                    nome = item["produto"].nome[:22]
                
                qtd      = item["quantidade"]
                unit     = item["preco_unitario"]
                subtotal = qtd * unit
                print(f"  {nome:<22} {qtd:>5} {unit:>8.2f} {subtotal:>10.2f}")

            # Totais da venda
            print("  " + "-" * 48)
            print(f"  Subtotal                          R$ {venda['subtotal']:>8.2f}")
            if venda["desconto_global"] > 0:
                economia = venda["subtotal"] - venda["total"]
                print(f"  Desconto ({venda['desconto_global']}%)               - R$ {economia:>8.2f}")
            print(f"  TOTAL                             R$ {venda['total']:>8.2f}")
            print("  " + "=" * 48)

            total_geral += venda["total"]

        # Resumo consolidado no final do relatório
        print(f"\n  TOTAL GERAL DE VENDAS         R$ {total_geral:>10.2f}")
        print(f"  Número de vendas realizadas  : {len(self.vendas_registradas)}")
        print("=" * 50 + "\n")

    # ── Relatório de estoque ─────────────────────────────────────────

    def relatorio_estoque(self):
        """
        Exibe a situação atual de todos os produtos em estoque:
        código, nome, categoria, quantidade e valor total do item.
        """
        if not self.estoque.produtos:
            print("O estoque está vazio.")
            return

        print("\n" + "=" * 60)
        print("               RELATÓRIO DE ESTOQUE")
        print("=" * 60)
        print(f"  {'CÓD':>5}  {'NOME':<22} {'CAT':<14} {'QTD':>5} {'UNIT':>8} {'TOTAL':>10}")
        print("-" * 60)

        valor_total_estoque = 0.0

        for item in self.estoque.produtos.values():
            produto    = item["produto"]
            quantidade = item["quantidade"]
            valor_item = produto.preco * quantidade   # valor total daquele produto no estoque

            print(
                f"  {produto.codigo:>5}  "
                f"{produto.nome[:22]:<22} "
                f"{produto.categoria[:14]:<14} "
                f"{quantidade:>5} "
                f"{produto.preco:>8.2f} "
                f"{valor_item:>10.2f}"
            )

            valor_total_estoque += valor_item

        print("-" * 60)
        print(f"  {'Valor total em estoque':<45} R$ {valor_total_estoque:>10.2f}")
        print(f"  Produtos cadastrados: {len(self.estoque.produtos)}")
        print("=" * 60 + "\n")

    # ── Histórico de movimentações ───────────────────────────────────

    def historico_movimentacoes(self):
        """
        Exibe o histórico completo de entradas e saídas do estoque,
        com data, tipo de operação, produto, quantidade e motivo.
        """
        historico = self.estoque.historico_movimentacoes

        if not historico:
            print("Nenhuma movimentação registrada no estoque.")
            return

        print("\n" + "=" * 65)
        print("           HISTÓRICO DE MOVIMENTAÇÕES DE ESTOQUE")
        print("=" * 65)
        print(f"  {'DATA/HORA':<20} {'TIPO':<8} {'CÓD':>5}  {'PRODUTO':<20} {'QTD':>5}  MOTIVO")
        print("-" * 65)

        # Itera sobre cada registro salvo pelo Estoque
        for mov in historico:
            tipo_fmt = "ENTRADA" if mov["tipo"] == "entrada" else "SAÍDA  "
            print(
                f"  {mov['data_hora']:<20} "
                f"{tipo_fmt:<8} "
                f"{mov['codigo']:>5}  "
                f"{mov['nome'][:20]:<20} "
                f"{mov['quantidade']:>5}  "
                f"{mov['motivo']}"
            )

        print("=" * 65)
        print(f"  Total de movimentações: {len(historico)}\n")

    # ── Persistência de dados ───────────────────────────────────────

    def salvar_relatorio(self, arquivo: str = "relatorio_vendas.json"):
        """
        Salva o histórico de vendas em arquivo JSON.

        Parâmetros:
            arquivo: caminho do arquivo JSON (padrão: 'relatorio_vendas.json')
        """
        try:
            dados = {
                "vendas_registradas": []
            }

            # Converte vendas para formato serializável
            for venda in self.vendas_registradas:
                venda_dados = {
                    "numero_venda": venda["numero_venda"],
                    "data_hora": venda["data_hora"],
                    "cliente": venda["cliente"],
                    "itens": [],
                    "subtotal": venda["subtotal"],
                    "desconto_global": venda["desconto_global"],
                    "total": venda["total"]
                }

                # Faz o mesmo para os itens da venda
                for item in venda["itens"]:
                    venda_dados["itens"].append({
                        "produto_nome": item["produto"].nome,
                        "produto_codigo": item["produto"].codigo,
                        "quantidade": item["quantidade"],
                        "preco_unitario": item["preco_unitario"]
                    })

                dados["vendas_registradas"].append(venda_dados)

            # Salva em JSON
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)

            print(f"✅ Relatório de vendas salvo com sucesso em '{arquivo}'.")

        except (IOError, OSError) as e:
            print(f"Erro ao salvar relatório: {e}")

    def carregar_relatorio(self, arquivo: str = "relatorio_vendas.json") -> bool:
        """
        Carrega o histórico de vendas a partir de arquivo JSON.
        Nota: Apenas carrega os dados para visualização/consulta.
        Não reconstrói objetos Venda, apenas os dados históricos.

        Parâmetros:
            arquivo: caminho do arquivo JSON (padrão: 'relatorio_vendas.json')

        Retorno:
            True se carregou com sucesso, False caso contrário
        """
        try:
            if not os.path.exists(arquivo):
                print(f"Arquivo '{arquivo}' não encontrado. Nenhuma venda anterior.")
                return False

            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Reconstrói o histórico de vendas em formato simplificado
            self.vendas_registradas = dados.get("vendas_registradas", [])

            print(f"✅ Relatório de vendas carregado com sucesso de '{arquivo}'.")
            return True

        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON em '{arquivo}'. Arquivo corrompido?")
            return False
        except (IOError, OSError) as e:
            print(f"Erro ao carregar relatório: {e}")
            return False