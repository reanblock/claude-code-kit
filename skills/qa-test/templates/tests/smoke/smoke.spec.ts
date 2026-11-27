// Generic smoke checks that suit most sites. Tailor them, and add project-specific
// checks, using the IDs from test-plan-smoke.md.
import { expect, test } from '@playwright/test';

test('SMK-01 home page loads', async ({ page }) => {
  const response = await page.goto('/');
  expect(response?.status(), 'HTTP status').toBeLessThan(400);
  await expect(page).toHaveTitle(/\S/);
  await expect(page.locator('body')).toBeVisible();
});

test('SMK-02 home page has no console errors', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  expect(errors, 'console errors').toEqual([]);
});

test('SMK-03 sample of internal links resolve', async ({ page, request, baseURL }) => {
  await page.goto('/');
  const origin = new URL(baseURL!).origin;
  const hrefs = await page.locator('a[href]').evaluateAll((as) => as.map((a) => (a as HTMLAnchorElement).href));
  const internal = [...new Set(hrefs)]
    .filter((h) => h.startsWith(origin) && !h.includes('#') && !/logout|sign-?out/i.test(h))
    .slice(0, 10);
  expect(internal.length, 'internal links found').toBeGreaterThan(0);
  for (const href of internal) {
    const res = await request.get(href);
    expect.soft(res.status(), href).toBeLessThan(400);
  }
});
