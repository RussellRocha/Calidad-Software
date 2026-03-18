import { Page, FrameLocator, expect } from '@playwright/test';

export class ProductPage{
  readonly page: Page;
  readonly frame: FrameLocator;

  constructor(page: Page) {
    this.page = page;
    this.frame = page.frameLocator('#framelive');
  }

  async goToHome() {
    await this.page.goto('https://demo.prestashop.com/#/en/front');
  }

  async selectFirstProduct() {
    const product = this.frame.locator('.js-product').first();
    await product.waitFor();
    await product.click();
  }

  async addToCartAndContinue() {
    const addBtn = this.frame.locator('[data-button-action="add-to-cart"]');
    const modal = this.frame.locator('#product-modal');

    await Promise.all([
        modal.waitFor({ state: 'visible' }), // 👈 esperar modal correcto
        addBtn.click()                       // 👈 acción que lo dispara
    ]);

    await modal.locator('button[data-dismiss="modal"]').click();

    await modal.waitFor({ state: 'hidden' });
    }

  async searchProduct(text: string) {
    const search = this.frame.locator('input[name="s"]');

    await search.waitFor();
    await search.fill(text);
    await search.press('Enter');
  }

  async selectProductByIndex(index: number) {
    const products = this.frame.locator('.js-product');

    await products.first().waitFor();
    await products.nth(index).click();
  }
    async addToCartAndCheckout() {
    const addBtn = this.frame.locator('[data-button-action="add-to-cart"]');
    const modal = this.frame.locator('#product-modal');

    await Promise.all([
        modal.waitFor({ state: 'visible' }),
        addBtn.click()
    ]);

    await modal.locator('a[href*="cart?action=show"]').click();
    }
}