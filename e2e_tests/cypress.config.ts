import { defineConfig } from 'cypress';
import createBundler from '@bahmutov/cypress-esbuild-preprocessor';
import { addCucumberPreprocessorPlugin } from '@badeball/cypress-cucumber-preprocessor';
import { createEsbuildPlugin } from '@badeball/cypress-cucumber-preprocessor/esbuild';
import * as dotenv from 'dotenv';
dotenv.config();

export default defineConfig({
  env: {
    FIXED_USER_USERNAME: process.env.FIXED_USER_USERNAME,
    FIXED_USER_EMAIL: process.env.FIXED_USER_EMAIL,
    FIXED_USER_PASSWORD: process.env.FIXED_USER_PASSWORD,
    DELETABLE_USER_USERNAME: process.env.DELETABLE_USER_USERNAME,
    DELETABLE_USER_EMAIL: process.env.DELETABLE_USER_EMAIL,
    DELETABLE_USER_PASSWORD: process.env.DELETABLE_USER_PASSWORD,
  },

  e2e: {
    baseUrl: process.env.BASE_URL || 'http://localhost:4200',
    specPattern: '**/*.feature',

    async setupNodeEvents(
      on: Cypress.PluginEvents,
      config: Cypress.PluginConfigOptions
    ): Promise<Cypress.PluginConfigOptions> {
      await addCucumberPreprocessorPlugin(on, config);
      on(
        'file:preprocessor',
        createBundler({
          plugins: [createEsbuildPlugin(config)],
        })
      );
      return config;
    },
  },
});
