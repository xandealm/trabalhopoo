# trabalhopoo
# Projeto de Gerenciamento de Restaurante

Este projeto implementa um sistema de gerenciamento de restaurante utilizando conceitos de Programação Orientada a Objetos (POO) em Python, com uma interface gráfica desenvolvida em `customtkinter`.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos Python, cada um representando uma classe ou funcionalidade específica:

- `cozinha.py`: Contém a classe `Cozinha` com métodos para listar pedidos para preparo.
- `garcom.py`: Contém a classe `Garcom`, que herda de `Pessoa`, com funcionalidades para garçons, incluindo cálculo de comissão.
- `mesa.py`: Contém a classe `Mesa` para gerenciar pedidos e o valor da conta de cada mesa.
- `pedido.py`: Contém a classe `Pedido` para representar os pedidos dos clientes e seu status.
- `pessoa.py`: Contém a classe base `Pessoa` para gerenciar informações de usuários (ID, nome, senha, papel).
- `prato.py`: Contém a classe `Prato` para representar os itens do menu do restaurante.
- `avaliacao.py`: Contém a classe `Avaliacao` para registrar avaliações do restaurante.
- `restaurante.py`: Contém a classe `Restaurante`, que agrega as mesas, garçons, pratos e avaliações, e gerencia o faturamento total.
- `interfacegrafica.py`: Implementa a interface gráfica do usuário (GUI) utilizando `customtkinter`, permitindo a interação com o sistema para diferentes perfis de usuário (dono, garçom, cozinheiro).

Além dos arquivos Python, o projeto utiliza arquivos JSON para persistência de dados:

- `json/dados.json`: Armazena os dados do restaurante, incluindo mesas, pedidos, garçons, pratos e avaliações.
- `json/funcionarios.json`: Armazena os dados de login dos funcionários.

## Funcionalidades Implementadas

As seguintes funcionalidades foram implementadas e integradas à interface gráfica:

### Painel do Dono
- **Visualização do Faturamento Total:** Exibe o faturamento acumulado do restaurante.
- **Visualização de Comissões dos Garçons:** Mostra o valor total vendido por cada garçom e sua respectiva comissão.
- **Zerar Expediente:** Permite reiniciar os dados de mesas e garçons para um novo expediente.
- **Adicionar Prato:** Funcionalidade para cadastrar novos pratos no menu do restaurante, incluindo nome, preço e tipo.
- **Avaliar Restaurante:** Permite registrar uma avaliação do restaurante com uma nota (0-5) e um comentário opcional.

### Painel do Garçom
- **Adicionar Novo Pedido:** Permite registrar pedidos para uma mesa específica, incluindo nome do pedido, tipo e valor. O pedido é enviado para a cozinha e o valor é adicionado à conta da mesa.
- **Visualizar Pedidos Prontos:** Exibe os pedidos que foram marcados como prontos pela cozinha.

### Painel do Cozinheiro
- **Visualizar Solicitações de Pedidos:** Mostra os pedidos que foram feitos pelos garçons e que precisam ser preparados.
- **Marcar Pedido como Pronto:** Permite ao cozinheiro alterar o status de um pedido para "pronto", indicando que está pronto para ser entregue.

## Como Executar o Projeto

Para executar o projeto, siga os passos abaixo:

1.  **Pré-requisitos:**
    - Python 3.x instalado.
    - `pip` (gerenciador de pacotes do Python) instalado.

2.  **Instalar Dependências:**
    Abra o terminal na pasta raiz do projeto e execute os seguintes comandos para instalar as bibliotecas necessárias:
    ```bash
    pip install customtkinter Pillow
    sudo apt-get update
    sudo apt-get install -y python3-tk
    ```

3.  **Estrutura de Pastas:**
    Certifique-se de que a estrutura de pastas esteja organizada da seguinte forma:
    ```
    . (pasta raiz do projeto)
    ├── cozinha.py
    ├── garcom.py
    ├── mesa.py
    ├── pedido.py
    ├── pessoa.py
    ├── prato.py
    ├── avaliacao.py
    ├── restaurante.py
    ├── interfacegrafica.py
    └── json/
        ├── dados.json
        └── funcionarios.json
    ```
    *Nota: A pasta `imagens` e o arquivo `restaurante_bomdegarfoimg.png` são opcionais e podem ser removidos ou substituídos se não forem utilizados.* 

4.  **Executar a Aplicação:**
    No terminal, na pasta raiz do projeto, execute o arquivo `interfacegrafica.py`:
    ```bash
    python3 interfacegrafica.py
    ```

    A tela de login será exibida. Você pode usar as credenciais do arquivo `json/funcionarios.json` para acessar os diferentes painéis (dono, garçom, cozinheiro).

## Validações

As validações de entrada do usuário foram implementadas para garantir a integridade dos dados, como:
- Verificação de campos vazios.
- Validação de tipos de dados (números inteiros para mesa, números decimais para valores).
- Validação de faixa de valores (ex: nota de avaliação entre 0 e 5).
- Verificação da existência de mesas ao adicionar pedidos.

## Testes

Para testar as funcionalidades, você pode:
- Fazer login com diferentes perfis (dono, garçom, cozinheiro).
- Adicionar pratos e verificar se aparecem no painel do dono.
- Fazer pedidos como garçom e verificar se aparecem no painel do cozinheiro.
- Marcar pedidos como prontos como cozinheiro e verificar se aparecem no painel do garçom.
- Avaliar o restaurante e verificar se a avaliação é registrada no painel do dono.
- Zerar o expediente e verificar se os dados são resetados.

## Observações

- A persistência dos dados é feita através dos arquivos `dados.json` e `funcionarios.json`.
- As classes foram adaptadas para incluir métodos `to_dict()` e `from_dict()` para facilitar a serialização e desserialização para JSON.
- A integração entre as classes e a interface gráfica foi realizada para que as operações na GUI manipulem os objetos das classes corretamente e os dados sejam salvos e carregados de forma consistente.
