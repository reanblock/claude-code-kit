// Reads qa.config.json and the environment variables for the current run.
// Shared by playwright.config.ts, auth.setup.ts and the specs.
import fs from 'node:fs';
import path from 'node:path';

type EnvConfig = { url: string };
type QaConfig = {
  project: string;
  environments: Record<string, EnvConfig>;
  auth?: { required?: boolean; loginPath?: string };
  testDataPrefix?: string;
};

export const qaConfig: QaConfig = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'qa.config.json'), 'utf8'),
);

export const env = (process.env.QA_ENV ?? 'uat').toLowerCase();
const envConfig = qaConfig.environments[env];
if (!envConfig && !process.env.QA_BASE_URL) {
  throw new Error(`Unknown QA_ENV "${env}". Add it to qa.config.json or set QA_BASE_URL.`);
}

export const baseURL = process.env.QA_BASE_URL ?? envConfig.url;
export const isProd = env === 'prod';

/** Tests tagged @writes create or change data. In PROD they only run when explicitly allowed. */
export const allowWrites = !isProd || process.env.QA_ALLOW_PROD_WRITES === 'yes';

export const authRequired = Boolean(qaConfig.auth?.required);
export const loginPath = qaConfig.auth?.loginPath ?? '/login';
export const authFile = path.join(__dirname, '.auth', `${env}.json`);

/** Credentials come from QA_<ENV>_USERNAME / QA_<ENV>_PASSWORD. Never commit them. */
export function credentials(): { username: string; password: string } {
  const key = env.toUpperCase();
  const username = process.env[`QA_${key}_USERNAME`];
  const password = process.env[`QA_${key}_PASSWORD`];
  if (!username || !password) {
    throw new Error(`Set QA_${key}_USERNAME and QA_${key}_PASSWORD to log in.`);
  }
  return { username, password };
}

/** Prefix every record a test creates with this, so test data is easy to find and clean up. */
export const testDataPrefix = `${qaConfig.testDataPrefix ?? 'QA-TEST'}-${new Date()
  .toISOString()
  .replace(/[-:T]/g, '')
  .slice(0, 12)}`;
