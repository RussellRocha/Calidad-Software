import { Page, Locator } from '@playwright/test';

export class AccountPage {
  readonly page: Page;
  readonly continueButton: Locator;
  readonly logoffLink: Locator;
  readonly mainText: Locator;

  constructor(page: Page) {
    this.page = page;
    this.continueButton = page.getByRole('link', { name: 'Continue' });
    this.logoffLink = page.locator('#maincontainer').getByRole('link', { name: 'Logoff' });
    this.mainText = page.locator('span.maintext');
  }

  async confirmSuccess() {
    await this.continueButton.first().click();
  }

  async logout() {
    await this.logoffLink.click();
    await this.continueButton.click();
  }
}