# E-Shop Brasil: Prova de Conceito (PoC) - Big Data e NoSQL

Este projeto é a entrega da Parte Prática da disciplina "Advanced Databases and Big Data". [cite_start]Ele simula uma solução para os desafios de gestão de dados e logística da E-Shop Brasil[cite: 61, 68].

## [cite_start]1. Introdução: Contexto e Objetivos [cite: 78]

[cite_start]A E-Shop Brasil enfrenta desafios de personalização [cite: 13][cite_start], otimização logística [cite_start]e segurança de dados devido ao seu grande volume de operações.

[cite_start]O objetivo desta aplicação é demonstrar como tecnologias NoSQL (MongoDB) e ferramentas de visualização (Streamlit), orquestradas com Docker, podem ser usadas para simular a gestão e análise de grandes volumes de dados (Big Data).

## [cite_start]2. Tecnologias Utilizadas [cite: 79]

- [cite_start]**MongoDB:** Banco de dados NoSQL orientado a documentos, escolhido por sua flexibilidade de esquema, ideal para armazenar catálogos de produtos, perfis de usuário e logs de comportamento.
- [cite_start]**Streamlit:** Biblioteca Python usada para criar rapidamente a interface gráfica (GUI) de análise e manipulação dos dados.
- [cite_start]**Docker & Docker Compose:** Utilizados para criar um ambiente de desenvolvimento e produção conteinerizado, garantindo que a aplicação e o banco de dados sejam escaláveis e fáceis de implantar.

## 3. Descrição da Aplicação

A aplicação `app.py` cria um painel de administração que se conecta ao banco MongoDB e permite as seguintes operações obrigatórias:

- [cite_start]**Inserção de Dados:** [cite: 83, 92] Na tela "Visão Geral", há um botão para popular o banco com dados falsos (produtos, usuários e logs) usando a biblioteca Faker.
- [cite_start]**Manipulação (Edição e Exclusão):** [cite: 84, 93] Na tela "Gerenciar Dados (CRUD)", é possível selecionar uma coleção, escolher um documento pelo `_id` e editá-lo ou excluí-lo.
- [cite_start]**Consultas e Exibição:** [cite: 85, 95] Os dados de todas as coleções são consultados (`find()`) e exibidos em tabelas interativas do Streamlit.
- [cite_start]**"Concatenação" (Agregação):** [cite: 84, 94] A "concatenação" ou manipulação avançada é demonstrada na tela "Análise de Big Data" através de _pipelines_ de agregação do MongoDB. São feitas duas análises:
  1.  [cite_start]**Análise de Estoque:** Agrupa produtos por categoria e soma o estoque (simulando otimização logística ).
  2.  [cite_start]**Análise de Logs:** Agrupa logs por tipo de ação do usuário (simulando análise de personalização ).

## [cite_start]4. Comandos para Execução [cite: 86]

Para executar o projeto localmente, você precisa ter o Docker e o Docker Compose instalados.

1.  Clone este repositório:

    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DA_PASTA]
    ```

2.  Suba os contêineres do MongoDB e da aplicação:

    ```bash
    docker-compose up -d --build
    ```

    _(O comando `docker-compose up` [cite: 87] é o solicitado)_

3.  Acesse a aplicação no seu navegador:
    [http://localhost:8501](http://localhost:8501)

4.  Para parar a aplicação:
    ```bash
    docker-compose down
    ```

## [cite_start]5. Exemplos e Testes [cite: 89, 90]

_(Nesta seção, você deve adicionar os prints ou GIFs solicitados)_

**Exemplo: Análise de Estoque por Categoria**
_(Aqui você colocaria um print da tela "Análise de Big Data" mostrando o gráfico de barras do estoque)_

**Exemplo: Edição de Produto**
_(Aqui você colocaria um GIF mostrando o processo de selecionar um produto, alterar o preço e salvar)_
