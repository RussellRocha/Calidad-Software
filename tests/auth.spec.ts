import { test, expect } from '@playwright/test';
import { AuthPage } from '../pages/AuthPage';
import { HomePage } from '../pages/HomePage';
import { ProductPage } from '../pages/ProductPage';
import { generateStrongPassword } from '../utils/dataGenerator';

test('Flujo E2E Prestashop', async ({ page }) => {
  const home = new HomePage(page);
  const auth = new AuthPage(page);
  const product = new ProductPage(page);

  const userData = {
    firstName: 'Russell',
    lastName: 'Rocha',
    email: `tester${Date.now()}@gmail.com`,
    password: generateStrongPassword()
  };

  await home.goTo();

  await auth.createAccount(userData);

  // ✅ Validación login (forma correcta en esta web)
  await expect(auth.frame.locator('a.logout')).toBeVisible();

});