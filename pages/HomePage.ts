import { BasePage } from './BasePage';

export class HomePage extends BasePage {

  async goToLogin() {
    await this.frame.locator('a:has-text("Sign in")').click();
  }

  async search(product: string) {
    const input = this.frame.locator('input[placeholder="Search our catalog"]');
    await input.fill(product);
    await input.press('Enter');
  }

  async goToWomen() {
    await this.frame.locator('#category-3 > a').hover();
    await this.frame.locator('#category-4 > a').click();
  }

  async changeLanguageToSpanish() {
    await this.frame.locator('#_desktop_language_selector').click();
    await this.frame.locator('a[data-iso-code="es"]').click();
  }
}