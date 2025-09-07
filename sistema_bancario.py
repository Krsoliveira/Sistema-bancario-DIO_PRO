import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class ContasIterador:
    """Iterador para percorrer as contas de um cliente."""
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._contas):
            conta = self._contas[self._index]
            self._index += 1
            return conta
        else:
            raise StopIteration

class Cliente:
    """
    Classe que representa um cliente do banco.
    Gerencia o relacionamento do cliente com suas contas.
    """
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Executa uma transação em uma conta do cliente."""
        if conta in self.contas:
            transacao.registrar(conta)
        else:
            print("\n❌ Operação falhou! A conta informada não pertence a este cliente.")

    def adicionar_conta(self, conta):
        """Adiciona uma nova conta para o cliente."""
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """
    Classe que representa um cliente do tipo Pessoa Física.
    Herda da classe Cliente e adiciona atributos específicos.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"

class Conta:
    """
    Classe base para contas bancárias.
    Define os atributos e métodos comuns a todas as contas.
    """
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de fábrica para criar uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque na conta.
        Retorna True se o saque for bem-sucedido, False caso contrário.
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n❌ Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n✅ Saque realizado com sucesso!")
            return True
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
        
        return False

    def depositar(self, valor):
        """
        Realiza um depósito na conta.
        Retorna True se o depósito for bem-sucedido, False caso contrário.
        """
        if valor > 0:
            self._saldo += valor
            print("\n✅ Depósito realizado com sucesso!")
            return True
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
            return False

class ContaCorrente(Conta):
    """
    Classe que representa uma conta corrente.
    Herda da classe Conta e adiciona limites específicos.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """
        Sobrescreve o método sacar para incluir validações de limite
        e número de saques diários.
        """
        # Conta quantos saques já foram feitos hoje
        saques_hoje = [
            transacao for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        ]
        
        excedeu_limite = valor > self._limite
        excedeu_saques = len(saques_hoje) >= self._limite_saques

        if excedeu_limite:
            print(f"\n❌ Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
        elif excedeu_saques:
            print("\n❌ Operação falhou! Número máximo de saques diários excedido.")
        else:
            # Chama o método sacar da classe pai (Conta)
            return super().sacar(valor)

        return False

    def __repr__(self):
        """Representação textual da conta para exibição."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    """Classe que gerencia o histórico de transações de uma conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma nova transação ao histórico."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    """Classe abstrata (Interface) para transações."""
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    """Classe para transações de saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra a transação de saque na conta."""
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    """Classe para transações de depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra a transação de depósito na conta."""
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# --- FUNÇÕES AUXILIARES (Lógica do Menu) ---

def log_transacao(func):
    """Decorator para logar transações (exemplo de funcionalidade extra)."""
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        # Aqui poderia salvar em um arquivo de log
        return resultado
    return envelope

def menu():
    """Exibe o menu de opções para o usuário."""
    menu_texto = """\n
    ================ MENU ================
    [c]\tCriar Cliente
    [n]\tCriar Conta
    [l]\tListar Contas
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def filtrar_cliente(cpf, clientes):
    """Busca um cliente na lista pelo CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    """
    Permite que o usuário selecione uma conta dentre as do cliente.
    Retorna a conta selecionada ou None se nenhuma for selecionada.
    """
    if not cliente.contas:
        print("\n❌ Cliente não possui conta!")
        return None
    
    # Se tiver só uma conta, retorna automaticamente
    if len(cliente.contas) == 1:
        return cliente.contas[0]

    # Pede para o usuário escolher se houver múltiplas contas
    print("\nEste cliente possui mais de uma conta. Por favor, selecione uma:")
    for i, conta in enumerate(cliente.contas):
        print(f"  [{i + 1}] Agência: {conta.agencia}, C/C: {conta.numero}")

    try:
        escolha = int(input("Digite o número da opção desejada: "))
        if 1 <= escolha <= len(cliente.contas):
            return cliente.contas[escolha - 1]
        else:
            print("\n❌ Opção inválida. Tente novamente.")
            return None
    except ValueError:
        print("\n❌ Entrada inválida. Por favor, digite um número.")
        return None

@log_transacao
def criar_cliente(clientes):
    """Cria um novo cliente (PessoaFisica) e o adiciona à lista."""
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n❌ Já existe cliente com este CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n✅ Cliente criado com sucesso!")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    """Cria uma nova conta corrente e a vincula a um cliente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return numero_conta

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n✅ Conta criada com sucesso!")
    return numero_conta + 1

def listar_contas(contas):
    """Exibe todas as contas cadastradas."""
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in ContasIterador(contas):
        print(textwrap.dedent(str(conta)))
        print("-" * 45)

@log_transacao
def depositar(clientes):
    """Realiza um depósito na conta de um cliente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        transacao = Deposito(valor)
        conta = recuperar_conta_cliente(cliente)
        
        if conta:
            cliente.realizar_transacao(conta, transacao)

    except ValueError:
        print("\n❌ Entrada inválida. Por favor, informe um valor numérico.")

@log_transacao
def sacar(clientes):
    """Realiza um saque na conta de um cliente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do saque: R$ "))
        transacao = Saque(valor)
        conta = recuperar_conta_cliente(cliente)
        
        if conta:
            cliente.realizar_transacao(conta, transacao)
    
    except ValueError:
        print("\n❌ Entrada inválida. Por favor, informe um valor numérico.")

@log_transacao
def mostrar_extrato(clientes):
    """Exibe o extrato da conta de um cliente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n[{transacao['data']}] {transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    """Função principal que executa o sistema bancário."""
    clientes = []
    contas = []
    numero_conta_atual = 1

    while True:
        opcao = menu()

        if opcao == "c":
            criar_cliente(clientes)
        elif opcao == "n":
            numero_conta_atual = criar_conta(numero_conta_atual, clientes, contas)
        elif opcao == "l":
            listar_contas(contas)
        elif opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            mostrar_extrato(clientes)
        elif opcao == "q":
            print("\nSaindo do sistema... Obrigado por usar nosso banco!\n")
            break
        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()