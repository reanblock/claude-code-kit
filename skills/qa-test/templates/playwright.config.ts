import { defineConfig, devices } from '@playwright/test';
import path from 'node:path';
import { allowWrites, authFile, authRequired, baseURL, isProd } from './qa-settings';

// Hard stop so a PROD run never starts by accident, with or without AI driving it.
if (isProd && process.env.QA_CONFIRM_PROD !== 'yes') {
  throw new Error('Refusing to run against PROD. Set QA_CONFIRM_PROD=yes to confirm.');
}

const runDir = process.env.QA_RUN_DIR ?? path.join(__dirname, 'reports', 'latest');
const dependencies = authRequired ? ['setup'] : [];
const browser = {
  ...devices['Desktop Chrome'],
  ...(authRequired ? { storageState: authFile } : {}),
};

export default defineConfig({
  timeout: 30_000,
  expect: { timeout: 10_000 },
  retries: 1,
  fullyParallel: true,
  workers: isProd ? 2 : undefined, // go easy on production
  outputDir: path.join(runDir, 'test-results'),
  reporter: [
    ['list'],
    ['json', { outputFile: path.join(runDir, 'results.json') }],
    ['html', { outputFolder: path.join(runDir, 'playwright-report'), open: 'never' }],
  ],
  grepInvert: allowWrites ? undefined : /@writes/,
  use: {
    baseURL,
    headless: true,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    ...(authRequired
      ? [{ name: 'setup', testDir: './tests', testMatch: /auth\.setup\.ts/, use: devices['Desktop Chrome'] }]
      : []),
    { name: 'smoke', testDir: './tests/smoke', dependencies, use: browser },
    { name: 'full', testDir: './tests', testIgnore: /auth\.setup\.ts/, dependencies, use: browser },
  ],
});
