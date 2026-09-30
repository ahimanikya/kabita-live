import { defineConfig } from 'astro/config';
export default defineConfig({
  output: 'static',
  site: process.env.SITE_URL || undefined,
  base: process.env.SITE_BASE || '/',
  publicDir: './.public',
  build: { format: 'file' },
  server: { host: '127.0.0.1' }
});
