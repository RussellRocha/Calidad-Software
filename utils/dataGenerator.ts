export function generateEmail() {
  return `test${Date.now()}@mail.com`;
}

export function generateStrongPassword() {
  const upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const lower = 'abcdefghijklmnopqrstuvwxyz';
  const numbers = '0123456789';
  const symbols = '!@#$%^&*';

  const pick = (str: string) => str[Math.floor(Math.random() * str.length)];

  let password =
    pick(upper) +
    pick(lower) +
    pick(numbers) +
    pick(symbols);

  // completar hasta 10 caracteres
  const all = upper + lower + numbers + symbols;
  for (let i = 0; i < 6; i++) {
    password += pick(all);
  }

  return password;
}