// Logs in once per run and saves the session for every other test.
// Adapt the selectors to the real login form.
import { expect, test as setup } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { authFile, credentials, loginPath } from '../qa-settings';

setup('log in', async ({ page }) => {
  const { username, password } = credentials();
  await page.goto(loginPath);
  await page.getByLabel(/email|username/i).fill(username);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole('button', { name: /log in|sign in/i }).click();
  await expect(page).not.toHaveURL(new RegExp(`${loginPath}$`));

  fs.mkdirSync(path.dirname(authFile), { recursive: true });
  await page.context().storageState({ path: authFile });
});
