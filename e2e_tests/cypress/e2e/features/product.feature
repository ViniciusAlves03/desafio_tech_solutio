#language: pt
Funcionalidade: Gestao de Produtos
  Como um usuário autenticado
  Quero poder listar, criar, visualizar, editar e excluir produtos
  Para gerir o meu inventario pessoal

  Contexto:
    Dado que estou logado no sistema
    E estou na listagem de produtos

  Cenário: Filtrar produtos por nome
    Quando digito "Alicate" no campo de pesquisa
    E clico em "Buscar"
    Então a tabela deve exibir apenas os produtos que contêm "Alicate"

  Cenário: Criar um novo produto com sucesso
    Quando clico em "Novo Produto"
    E preencho os dados do produto com Nome "Monitor 4K", Marca "LG", Preço "1500" e Quantidade "2"
    E clico em "Cadastrar Produto"
    Então devo ver uma notificação indicando que a criacao foi para a fila
    E o formulário de produto deve ser fechado
    Quando digito "Monitor 4K" no campo de pesquisa
    E clico em "Buscar"
    Então a tabela deve conter o produto "Monitor 4K"

  Cenário: Validação do formulário de produto
    Quando clico em "Novo Produto"
    E clico em "Cadastrar Produto" com o formulário em branco
    Então os campos obrigatorios do produto devem exibir mensagens de erro

  Cenário: Visualizar detalhes de um produto
    Quando clico na ação "Visualizar" do primeiro produto da lista
    Então um card de detalhes do produto deve abrir
    E devo ver o nome e o preço do produto

  Cenário: Excluir um produto
    Quando digito "Monitor 4K" no campo de pesquisa
    E clico em "Buscar"
    E guardo o ID do primeiro produto da lista
    E clico na ação "Excluir" do primeiro produto da lista
    E confirmo a exclusao do produto
    Então devo ver uma notificação indicando que a exclusao foi para a fila
    Quando digito "Monitor 4K" no campo de pesquisa
    E clico em "Buscar"
    Então a tabela não deve conter o produto com o ID guardado
