import { Page, FrameLocator } from '@playwright/test';

export class BasePage {
  protected page: Page;
  protected frame: FrameLocator;

  constructor(page: Page) {
    this.page = page;
    this.frame = page.frameLocator('#framelive');
  }

  async goTo() {
    await this.page.goto('https://demo.prestashop.com/#/en/front');
  }
}