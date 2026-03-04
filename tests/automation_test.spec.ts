import { test, expect } from '@playwright/test';

test('Happy Path: Registro y Login en Automation Test Store', async ({ page }) => {
  // Generar datos únicos
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

  // 1. Ir a la web y click en Login or register
  await page.goto('https://automationteststore.com/');
  await page.getByRole('link', { name: 'Login or register' }).click();

  // 2. Bajo "I am a new customer" click en Continue
  await page.getByRole('button', { name: 'Continue' }).click();

  // 3. Llenar todos los datos del formulario
  await page.locator('#AccountFrm_firstname').fill(userData.firstName);
  await page.locator('#AccountFrm_lastname').fill(userData.lastName);
  await page.locator('#AccountFrm_email').fill(userData.email);
  await page.locator('#AccountFrm_address_1').fill(userData.address);
  await page.locator('#AccountFrm_city').fill(userData.city);

  // --- FIX DE PAÍS Y REGIÓN ---
  await page.locator('#AccountFrm_country_id').selectOption({ index: 1 });
  
  const zoneId = page.locator('#AccountFrm_zone_id');
  await expect(async () => {
    const count = await zoneId.locator('option').count();
    expect(count).toBeGreaterThan(1);
  }).toPass(); 

  await zoneId.selectOption({ index: 1 });
  // -----------------------------

  await page.locator('#AccountFrm_postcode').fill(userData.zipCode);
  await page.locator('#AccountFrm_loginname').fill(userData.loginName);
  await page.locator('#AccountFrm_password').fill(userData.password);
  await page.locator('#AccountFrm_confirm').fill(userData.password);

  // 4. Newsletter subscribe: NO
  await page.locator('#AccountFrm_newsletter0').check();

  // 5. Click en el checkbox de Privacy Policy
  await page.locator('#AccountFrm_agree').check();

  // 6. Click en el boton Continue del formulario
  await page.getByRole('button', { name: 'Continue' }).click();

  // 7. Click en Continue (Confirmación de cuenta creada)
  // Usamos el de tu versión original que funcionaba
  await page.getByRole('link', { name: 'Continue' }).click();

  // 8. Ir al panel derecho y click en "Logoff" (Tu versión original)
  await page.locator('#maincontainer').getByRole('link', { name: 'Logoff' }).click();

  // 9. Click en continue
  await page.getByRole('link', { name: 'Continue' }).click();

  // 10. Click en Login or register
  await page.getByRole('link', { name: 'Login or register' }).click();

  // 11. Ingresar con las credenciales creadas
  await page.locator('#loginFrm_loginname').fill(userData.loginName);
  await page.locator('#loginFrm_password').fill(userData.password);

  // 12. Click en Login
  await page.getByRole('button', { name: 'Login' }).click();

  // Verificación final
  await expect(page.locator('span.maintext')).toContainText('My Account');
});