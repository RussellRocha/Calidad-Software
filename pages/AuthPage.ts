import { Page, FrameLocator } from '@playwright/test';

export class AuthPage {
  readonly page: Page;
  readonly frame: FrameLocator;

  constructor(page: Page) {
    this.page = page;
    this.frame = page.frameLocator('#framelive');
  }

  async goToLogin() {
    await this.frame.locator('a[href*="login"]').first().click();
  }

  async goToRegister() {
    await this.frame.locator('a:has-text("Create one here")').click();
  }

  async createAccount(user: any) {
    await this.goToLogin();
    await this.goToRegister();

    const form = this.frame.locator('#customer-form');

    await form.locator('input[name="firstname"]').fill(user.firstName);
    await form.locator('input[name="lastname"]').fill(user.lastName);
    await form.locator('input[name="email"]').fill(user.email);
    await form.locator('input[name="password"]').fill(user.password);

    await form.locator('input[name="psgdpr"]').check();
    await form.locator('input[name="customer_privacy"]').check();

    await form.locator('button[type="submit"]').click();
    }
}