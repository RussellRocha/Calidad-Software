import { test } from '@playwright/test';
import { ProductPage } from '../pages/ProductPage';

test('Cambiar idioma', async ({ page }) => {
  const product = new ProductPage(page);

  await product.goToHome();

  await product.frame.locator('#_desktop_language_selector').click();
  await product.frame.locator('a[data-iso-code="es"]').click();
});