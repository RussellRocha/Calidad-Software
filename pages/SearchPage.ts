import { BasePage } from './BasePage';

export class SearchPage extends BasePage {

  async selectResult(index: number) {
    await this.frame.locator('.product-miniature').nth(index).click();
  }
}