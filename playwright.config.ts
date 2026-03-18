import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  use: {
    headless: false,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  }
});