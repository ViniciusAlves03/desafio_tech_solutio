import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';

let dynamicUser = '';
let dynamicEmail = '';
const defaultPassword = 'senha123';

Given('que estou na página de registo', () => {
  cy.visit('/register');
});

Given('que estou na página de login', () => {
  cy.visit('/login');
});

Given('que estou logado no sistema', () => {
  const login = Cypress.env('FIXED_USER_EMAIL');
  const password = Cypress.env('FIXED_USER_PASSWORD');
  cy.visit('/login');
  cy.get('input[formControlName="login"]').clear().type(login);
  cy.get('input[formControlName="password"]').clear().type(password);
  cy.get('button[type="submit"]').contains('Entrar').click();
  cy.url().should('include', '/products');
});

When('preencho os dados de registo com um usuário dinâmico', () => {
  const timestamp = Date.now();
  dynamicUser = `user_${timestamp}`;
  dynamicEmail = `email_${timestamp}@teste.com`;

  cy.get('input[formControlName="username"]').type(dynamicUser);
  cy.get('input[formControlName="email"]').type(dynamicEmail);
  cy.get('input[formControlName="password"]').type(defaultPassword);
});

When('preencho os dados de login usando o meu {string} de teste', (tipoLogin: string) => {
  const password = Cypress.env('FIXED_USER_PASSWORD');
  let loginValue = '';

  if (tipoLogin === 'email') {
    loginValue = Cypress.env('FIXED_USER_EMAIL');
  } else if (tipoLogin === 'username') {
    loginValue = Cypress.env('FIXED_USER_USERNAME');
  }

  cy.get('input[formControlName="login"]').clear().type(loginValue);
  cy.get('input[formControlName="password"]').clear().type(password);
});

When('faço login com o usuário dinâmico recém-criado', () => {
  cy.get('input[formControlName="login"]').type(dynamicUser);
  cy.get('input[formControlName="password"]').type(defaultPassword);
  cy.get('button[type="submit"]').contains('Entrar').click();
});

When('preencho o "E-mail ou Username" com {string}', (login: string) => {
  cy.get('input[formControlName="login"]').type(login);
});

When('preencho a "Senha" com {string}', (password: string) => {
  cy.get('input[formControlName="password"]').type(password);
});

When('clico no botão {string}', (buttonText: string) => {
  cy.get('button').contains(buttonText).click();
});

When('clico no campo "Username" e saio sem preencher', () => {
  cy.get('input[formControlName="username"]').focus().blur();
});

When('clico no botão de "Sair" no cabeçalho', () => {
  cy.get('.btn-logout-header').click();
});

Then('devo ver uma notificação de sucesso', () => {
  cy.get('.toast-container.success').should('be.visible');
});

Then('devo ver uma notificação de erro {string}', (errorMessage: string) => {
  cy.get('.error-message')
    .should('be.visible')
    .and('contain.text', errorMessage);
});

Then('devo ver a mensagem de erro {string} sob o campo', (validationMessage: string) => {
  cy.get('.validation-error small')
    .should('be.visible')
    .and('contain.text', validationMessage);
});

Then('devo ser redirecionado para a página de login', () => {
  cy.url().should('include', '/login');
});

Then('devo ser redirecionado para a listagem de produtos', () => {
  cy.url().should('include', '/products');
});

Then('devo ver o cabeçalho com o menu do usuário', () => {
  cy.get('.user-menu-container').should('be.visible');
});
