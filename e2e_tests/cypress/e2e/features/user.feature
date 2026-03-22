# language: pt
Funcionalidade: Gestao da Conta de Usuário
  Como um usuário autenticado
  Quero poder visualizar, editar e excluir a minha conta
  Para manter os meus dados atualizados ou remover o meu acesso

  Cenário: Visualizar os dados do perfil
    Dado que estou logado no sistema como "usuario_fixo"
    Quando abro o menu do usuário
    E clico na opção "Visualizar Perfil"
    Então o card de usuário deve abrir
    E devo ver os detalhes do meu perfil

  Cenário: Editar dados da conta com sucesso
    Dado que estou logado no sistema como "usuario_fixo"
    Quando abro o menu do usuário
    E clico na opção "Editar Conta"
    E altero o campo "Username" do formulário para "usuario_editado"
    E clico no botão "Salvar Alterações"
    Então devo ver uma notificação de sucesso
    E a modal de usuário deve ser fechada

  Cenário: Excluir a conta e os produtos associados
    Dado que estou logado no sistema como "usuario_deletavel"
    Quando abro o menu do usuário
    E clico na opção "Excluir Conta"
    E confirmo a exclusão
    Então devo ver uma notificação de sucesso
    E devo ser redirecionado para a página de login
