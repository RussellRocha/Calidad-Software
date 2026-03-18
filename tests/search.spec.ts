import { test } from '@playwright/test';
import { ProductPage } from '../pages/ProductPage';

test('Buscar poster y comprar tercero', async ({ page }) => {
  const product = new ProductPage(page);

  await product.goToHome();

  const search = product.frame.locator('input[name="s"]');

  await search.fill('poster');
  await search.press('Enter');

  await product.frame.locator('#js-product-list').waitFor();

  const thirdProduct = product.frame.locator('.product-miniature').nth(2);
  await thirdProduct.click();

  // ✅ agregar
  await product.addToCartAndContinue();

  // ❗ finalizar compra
  await product.frame.locator('.blockcart').click();
  await product.frame.locator('a[href*="cart?action=show"]').click();
});