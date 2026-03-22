# language: pt
Funcionalidade: Autenticacao de Usuarios
  Como um visitante do sistema
  Quero poder registar-me, fazer login e logout
  Para gerir os meus produtos

  Cenário: Registo de um novo usuário com sucesso
    Dado que estou na página de registo
    Quando preencho os dados de registo com um usuário dinâmico
    E clico no botão "Criar a Minha Conta"
    Então devo ver uma notificação de sucesso
    E devo ser redirecionado para a página de login

  Cenário: Validação de campos obrigatórios no registo
    Dado que estou na página de registo
    Quando clico no campo "Username" e saio sem preencher
    Então devo ver a mensagem de erro "O nome de usuário é obrigatório." sob o campo

  Cenário: Login com credenciais inválidas
    Dado que estou na página de login
    Quando preencho o "E-mail ou Username" com "usuario_falso"
    E preencho a "Senha" com "senha_errada"
    E clico no botão "Entrar"
    Então devo ver uma notificação de erro "E-mail, usuário ou senha incorretos"

  Cenário: Login com credenciais válidas usando E-mail
    Dado que estou na página de login
    Quando preencho os dados de login usando o meu "email" de teste
    E clico no botão "Entrar"
    Então devo ser redirecionado para a listagem de produtos
    E devo ver o cabeçalho com o menu do usuário

  Cenário: Login com credenciais válidas usando Username
    Dado que estou na página de login
    Quando preencho os dados de login usando o meu "username" de teste
    E clico no botão "Entrar"
    Então devo ser redirecionado para a listagem de produtos
    E devo ver o cabeçalho com o menu do usuário

  Cenário: Logout do sistema
    Dado que estou logado no sistema
    Quando clico no botão de "Sair" no cabeçalho
    Então devo ser redirecionado para a página de login
