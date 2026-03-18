import { test } from '@playwright/test';
import { ProductPage } from '../pages/ProductPage';

test('Compra de 8 productos', async ({ page }) => {
  const product = new ProductPage(page);

  await product.goToHome();

  for (let i = 0; i < 8; i++) {
    await product.frame.locator('.product-miniature').nth(i % 4).click();

    await product.addToCart();

    await product.goToHome(); // volver al home
  }
});