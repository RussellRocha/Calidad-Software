import { test, expect } from '@playwright/test';
import { RegisterPage } from '../pages/RegisterPage';
import { LoginPage } from '../pages/LoginPage';
import { AccountPage } from '../pages/AccountPage';

test('Happy Path: Registro, Logout y Login con POM', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const registerPage = new RegisterPage(page);
  const accountPage = new AccountPage(page);

  const uniqueId = Date.now();
  const userData = {
    firstName: 'QA',
    lastName: 'Tester',
    email: `test${uniqueId}@example.com`,
    address: 'Calle Falsa 123',
    city: 'Cochabamba',
    zipCode: '0000',
    loginName: `user${uniqueId}`,
    password: 'Password123!'
  };

  // 1. Navegación e inicio de registro
  await loginPage.goToLogin();
  await loginPage.startRegistration();

  // 2. Registro de usuario
  await registerPage.fillRegistrationForm(userData);
  await accountPage.confirmSuccess();

  // 3. Logout
  await accountPage.logout();

  // 4. Re-Login con credenciales nuevas
  await loginPage.loginOrRegisterLink.click();
  await loginPage.login(userData.loginName, userData.password);

  // 5. Verificación final
  await expect(accountPage.mainText).toContainText('My Account');
});