# Sistema Bancário Simples - Desafio DIO PRO

Este projeto é uma implementação de um sistema bancário simples, desenvolvido como parte de um desafio do bootcamp da [DIO PRO](https://www.dio.me/). O objetivo é criar um sistema funcional que permita ao usuário realizar as operações básicas de uma conta bancária: depósito, saque e visualização de extrato.

## 📜 Descrição do Projeto

O sistema foi desenvolvido em Python e simula as operações de uma conta corrente. Ele controla o saldo, impõe um limite de valor por saque, um limite diário de número de saques e mantém um registro de todas as transações para exibição no extrato.

## ✨ Funcionalidades

O sistema oferece as seguintes operações:

  * **Depositar:** Permite ao usuário adicionar um valor à sua conta. Apenas valores positivos são aceitos.
  * **Sacar:** Permite ao usuário retirar um valor da sua conta, sujeito às seguintes regras:
      * O valor do saque não pode exceder o limite de R$ 500,00 por transação.
      * O usuário pode realizar no máximo 3 saques por dia.
      * O valor a ser sacado não pode ser maior que o saldo disponível em conta.
  * **Extrato:** Exibe um histórico de todas as transações (depósitos e saques) realizadas, finalizando com o saldo atual da conta.

## 🛠️ Tecnologias Utilizadas

  * **Linguagem:** Python 3

## ⚙️ Como Executar o Projeto

1.  **Clone o repositório (ou copie o código):**
    ```bash
    git clone https://seu-repositorio-aqui.git
    ```
2.  **Navegue até o diretório do projeto:**
    ```bash
    cd nome-do-diretorio
    ```
3.  **Execute o script Python:**
    ```bash
    python nome_do_seu_arquivo.py
    ```

O script já contém um exemplo de uso no final do arquivo que demonstra as funcionalidades de depósito, saque e extrato.

## Code O Código

O sistema é construído em torno de algumas variáveis globais e três funções principais:

### Variáveis Globais

  * `saldo`: Armazena o valor monetário atual da conta.
  * `limite_saque`: Define o valor máximo permitido para uma única operação de saque (R$ 500,00).
  * `saques_realizados`: Contador do número de saques efetuados no dia.
  * `limite_saques_diarios`: Define o número máximo de saques permitidos por dia (3).
  * `extrato`: Uma lista que armazena o registro de todas as operações realizadas.

### Funções

  * `depositar(valor)`: Adiciona o `valor` especificado ao `saldo` e registra a operação no `extrato`.
  * `sacar(valor)`: Subtrai o `valor` do `saldo` se todas as condições (limite por saque, limite diário e saldo suficiente) forem atendidas. Também registra a operação no `extrato`.
  * `mostrar_extrato()`: Imprime todas as operações registradas na variável `extrato` e, ao final, o `saldo` atual.

<!-- end list -->

```python
# Variáveis globais
saldo = 0
limite_saque = 500
saques_realizados = 0
limite_saques_diarios = 3
extrato = []

def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: +R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Valor inválido para depósito.")

def sacar(valor):
    global saldo, saques_realizados
    if saques_realizados >= limite_saques_diarios:
        print("Limite diário de saques atingido.")
    elif valor > limite_saque:
        print(f"Limite por saque é de R$ {limite_saque:.2f}.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor <= 0:
        print("Valor inválido para saque.")
    else:
        saldo -= valor
        saques_realizados += 1
        extrato.append(f"Saque: -R$ {valor:.2f}")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")

def mostrar_extrato():
    print("\n📄 Extrato Bancário:")
    if not extrato:
        print("Nenhuma movimentação realizada.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}\n")

# Exemplo de uso
depositar(1000)
sacar(200)
sacar(300)
sacar(100)
mostrar_extrato()

```

## ✒️ Autor

Projeto desenvolvido por Kaique Rafael Dos Santos Oliveira como parte do bootcamp da DIO PRO.
