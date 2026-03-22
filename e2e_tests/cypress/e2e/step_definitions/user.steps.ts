import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';

Given('que estou logado no sistema como {string}', (userType: string) => {
  const prefix = userType === 'usuario_deletavel' ? 'DELETABLE_USER' : 'FIXED_USER';
  const login = Cypress.env(`${prefix}_EMAIL`);
  const password = Cypress.env(`${prefix}_PASSWORD`);

  cy.visit('/login');
  cy.get('input[formControlName="login"]').clear().type(login);
  cy.get('input[formControlName="password"]').clear().type(password);
  cy.get('button[type="submit"]').contains('Entrar').click();
  cy.url().should('include', '/products');
});

When('abro o menu do usuário', () => {
  cy.get('.btn-user-icon').click();
});

When('clico na opção {string}', (option: string) => {
  cy.get('.dropdown-menu button').contains(option).click();
});

When('altero o campo {string} do formulário para {string}', (field: string, price: string) => {
  const controlName = field.toLowerCase();
  cy.get(`.user-modal input[formControlName="${controlName}"]`).clear().type(price);
});

When('clico no botao {string} ', (buttonText: string) => {
  cy.get('.user-modal .btn-confirm').contains(buttonText).click();
});

When('confirmo a exclusão', () => {
  cy.get('.modal-overlay .btn-confirm').contains('Sim, Confirmar').click();
});

Then('o card de usuário deve abrir', () => {
  cy.get('.user-modal').should('be.visible');
});

Then('devo ver os detalhes do meu perfil', () => {
  cy.get('.user-details').should('be.visible');
  cy.get('.user-details p').should('have.length.at.least', 2);
});

Then('a modal de usuário deve ser fechada', () => {
  cy.get('.user-modal').should('not.exist');
});
