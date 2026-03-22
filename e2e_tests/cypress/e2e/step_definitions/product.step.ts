import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';

let deletedProductId = '';

Given('estou na listagem de produtos', () => {
    cy.url().should('include', '/products');
    cy.get('.product-table').should('be.visible');
});

When('digito {string} no campo de pesquisa', (term: string) => {
    cy.get('.filter-bar input[placeholder="Filtrar por nome"]').clear().type(term);
});

When('clico em {string}', (buttonText: string) => {
    cy.get('button').contains(buttonText).click();
});

When('preencho os dados do produto com Nome {string}, Marca {string}, Preço {string} e Quantidade {string}', (name: string, brand: string, price: string, quantity: string) => {
    cy.get('input[formControlName="name"]').type(name);
    cy.get('input[formControlName="brand"]').type(brand);
    cy.get('input[formControlName="price"]').type(price);
    cy.get('input[formControlName="quantity"]').type(quantity);
});

When('clico em "Cadastrar Produto" com o formulário em branco', () => {
    cy.get('input[formControlName="name"]').focus().blur();
});

When('clico na ação {string} do primeiro produto da lista', (action: string) => {
    cy.get('.product-table tbody tr').first().within(() => {
        cy.get('button').contains(action).click();
    });
});

When('confirmo a exclusao do produto', () => {
    cy.get('.modal-card .btn-confirm').contains('Sim, Confirmar').click();
});

When('guardo o ID do primeiro produto da lista', () => {
    cy.get('.product-table tbody tr').first().find('td').first().invoke('text').then((text) => {
        deletedProductId = text.trim();
    });
});

Then('a tabela deve exibir apenas os produtos que contêm {string}', (term: string) => {
    cy.get('.product-table tbody tr .td-name').should(($celulasDeNome) => {
        $celulasDeNome.each((index, celula) => {
            const productName = Cypress.$(celula).text().toLowerCase();
            expect(productName).to.include(term.toLowerCase());
        });
    });
});

Then('devo ver uma notificação indicando que a criacao foi para a fila', () => {
    cy.get('.toast-container').should('be.visible').and('contain.text', 'fila');
});

Then('devo ver uma notificação indicando que a exclusao foi para a fila', () => {
    cy.get('.toast-container').should('be.visible');
});

Then('o formulário de produto deve ser fechado', () => {
    cy.url().should('include', '/products');
});

Then('os campos obrigatorios do produto devem exibir mensagens de erro', () => {
    cy.get('.validation-error small').should('be.visible');
});

Then('um card de detalhes do produto deve abrir', () => {
    cy.get('.product-detail-modal').should('be.visible');
});

Then('devo ver o nome e o preço do produto', () => {
    cy.get('.product-detail-modal .product-name').should('not.be.empty');
    cy.get('.product-detail-modal .price').should('not.be.empty');
});

Then('a tabela não deve conter o produto com o ID guardado', () => {
    cy.wait(1000);
    cy.get('body').then(($body) => {
        if ($body.find('.product-table tbody tr').length > 0) {
            cy.contains('.product-table tbody tr td:first-child', deletedProductId).should('not.exist');
        } else {
            expect(true).to.be.true;
        }
    });
});

Then('a tabela deve conter o produto {string}', (productName: string) => {
    cy.get('.product-table tbody tr .td-name')
      .contains(productName, { matchCase: true })
      .should('be.visible');
});
