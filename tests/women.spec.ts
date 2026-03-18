import { test } from '@playwright/test';
import { ProductPage } from '../pages/ProductPage';

test('Compra en Women', async ({ page }) => {
  const product = new ProductPage(page);

  await product.goToHome();

  await product.frame.getByRole('link', { name: 'Clothes' }).click();
  await product.frame.getByRole('link', { name: 'Women' }).click();

  await product.frame.locator('.product-miniature').first().click();

  // ✅ agregar producto
  await product.addToCartAndContinue();

  // ❗ ahora sí finalizar compra
  await product.frame.locator('.blockcart').click(); // abrir carrito

  await product.frame.locator('a[href*="cart?action=show"]').click();
});