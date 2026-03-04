import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly loginOrRegisterLink: Locator;
  readonly continueRegisterButton: Locator;
  readonly loginNameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.loginOrRegisterLink = page.getByRole('link', { name: 'Login or register' });
    this.continueRegisterButton = page.getByRole('button', { name: 'Continue' });
    this.loginNameInput = page.locator('#loginFrm_loginname');
    this.passwordInput = page.locator('#loginFrm_password');
    this.loginButton = page.getByRole('button', { name: 'Login' });
  }

  async goToLogin() {
    await this.page.goto('https://automationteststore.com/');
    await this.loginOrRegisterLink.click();
  }

  async startRegistration() {
    await this.continueRegisterButton.click();
  }

  async login(user: string, pass: string) {
    await this.loginNameInput.fill(user);
    await this.passwordInput.fill(pass);
    await this.loginButton.click();
  }
}