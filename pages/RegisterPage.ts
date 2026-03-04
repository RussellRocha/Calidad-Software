import { Page, Locator, expect } from '@playwright/test';

export class RegisterPage {
  readonly page: Page;
  readonly firstNameInput: Locator;
  readonly lastNameInput: Locator;
  readonly emailInput: Locator;
  readonly addressInput: Locator;
  readonly cityInput: Locator;
  readonly countrySelect: Locator;
  readonly zoneSelect: Locator;
  readonly zipCodeInput: Locator;
  readonly loginNameInput: Locator;
  readonly passwordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly newsletterRadio: Locator;
  readonly agreeCheckbox: Locator;
  readonly continueButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.firstNameInput = page.locator('#AccountFrm_firstname');
    this.lastNameInput = page.locator('#AccountFrm_lastname');
    this.emailInput = page.locator('#AccountFrm_email');
    this.addressInput = page.locator('#AccountFrm_address_1');
    this.cityInput = page.locator('#AccountFrm_city');
    this.countrySelect = page.locator('#AccountFrm_country_id');
    this.zoneSelect = page.locator('#AccountFrm_zone_id');
    this.zipCodeInput = page.locator('#AccountFrm_postcode');
    this.loginNameInput = page.locator('#AccountFrm_loginname');
    this.passwordInput = page.locator('#AccountFrm_password');
    this.confirmPasswordInput = page.locator('#AccountFrm_confirm');
    this.newsletterRadio = page.locator('#AccountFrm_newsletter0');
    this.agreeCheckbox = page.locator('#AccountFrm_agree');
    this.continueButton = page.getByRole('button', { name: 'Continue' });
  }

  async fillRegistrationForm(userData: any) {
    await this.firstNameInput.fill(userData.firstName);
    await this.lastNameInput.fill(userData.lastName);
    await this.emailInput.fill(userData.email);
    await this.addressInput.fill(userData.address);
    await this.cityInput.fill(userData.city);
    
    // Selección de país y espera de zonas
    await this.countrySelect.selectOption({ index: 1 });
    await expect(async () => {
      const count = await this.zoneSelect.locator('option').count();
      expect(count).toBeGreaterThan(1);
    }).toPass();
    await this.zoneSelect.selectOption({ index: 1 });

    await this.zipCodeInput.fill(userData.zipCode);
    await this.loginNameInput.fill(userData.loginName);
    await this.passwordInput.fill(userData.password);
    await this.confirmPasswordInput.fill(userData.password);
    
    await this.newsletterRadio.click();
    await this.agreeCheckbox.check();
    await this.continueButton.click();
  }
}