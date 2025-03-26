# TESTE DE API

Este repositório contém um teste de API que inclui o desenvolvimento de uma interface web utilizando Vue.js que interage com um servidor em Python para realizar buscas pela razão social das Operadoras Ativas na ANS no formato CSV registradas no arquivo Relatorio_cadop.csv disponível em [Dados cadastrais das Operadoras Ativas na ANS](https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/).

## Descrição

O objetivo deste projeto é:
- Utilizar o CSV obtido no item 3.2. do teste para realizar buscas textuais na lista de cadastros de operadoras.
- Implementar um servidor em Python com uma rota capaz de buscar os registros mais relevantes.
- Demonstrar os resultados utilizando uma coleção no Postman.

## Estrutura do Projeto

- **backend**: Contém o código do servidor Python.
- **frontend**: Contém a interface web desenvolvida em Vue.js.

## Configuração do Ambiente

Siga as instruções abaixo para configurar e executar o projeto:

### Passos para Instalação

1. Clone este repositório para sua máquina local:
   ```bash
   git clone <URL_DO_REPOSITORIO>

2. Instale os pacotes necessários:

 - Para o backend:

    - Certifique-se de que o Python está instalado.

    - Entre na pasta backend e execute: `pip install flask`

 - Para o frontend
     
    - Certifique-se de que o Node.js e o npm estão instalados.

    - Entre na pasta frontend e execute: `pm install vue axios`


## Executando o Projeto

Entre na pasta backend utilizando o terminal e execute : `python server.py`

Entre na pasta frontend utilizando o terminal e execute : `npm run serve`


## Testando a Aplicação

- Interface Web: Use a interface web para interagir com o servidor e realizar buscas textuais.

- Postman: Para testar diretamente as rotas do servidor:

- Importe a coleção do Postman fornecida.

- Faça requisições às rotas configuradas e verifique os resultados.

## API - Backend em Flask

Esta API foi desenvolvida utilizando o framework Flask e tem como objetivo realizar buscas textuais em uma lista de cadastros de operadoras, retornando os registros mais relevantes.

### Estrutura da API

#### Endpoints

- **`GET /operadoras`**:
  - **Descrição**: Realiza uma busca textual na lista de cadastros de operadoras.
  - **Parâmetros**:
    - `query` (string): Texto a ser buscado nos registros de `Razao_Social`.
  - **Retorno**:
    - JSON contendo os 10 registros mais relevantes que correspondem à busca. Substitui valores `NaN` por `"Não informado"`.
   
## Frontend - Interface em Vue.js

A interface web foi desenvolvida em Vue.js e permite aos usuários realizar buscas textuais de operadoras e exibir os resultados em cartões organizados.

---

### Estrutura do Componente

#### Template
O HTML do componente é responsável por renderizar a interface com os seguintes elementos:
- **Campo de busca**: Input para a Razão Social da operadora.
- **Botão de busca**: Dispara a consulta ao backend.
- **Cartões**: Exibem as informações das operadoras retornadas pela API.

## Dependências

 - Vue.js: Framework JavaScript para desenvolvimento da interface web.

 - Axios: Biblioteca JavaScript para realizar requisições HTTP.

 - Python: Necessário para rodar o servidor backend.

 - Flask: Framework para desenvolvimento do servidor em Python.

## Exemplo de Funcionamento da API

Abaixo estão imagens demonstrando o funcionamento da aplicação e os filtros em ação:

### Busca por Razão Social
![Busca por Razão Social](img-readme/busca-razao-social.png)

### Seleção de Ordenação
![Seleção de Ordenação Ascendente](img-readme/ordenacaoasc.png)

![Seleção de Ordenação Descendente](img-readme/ordenacaodesc.png)
