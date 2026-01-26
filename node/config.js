'use strict';

const dotenv = require('dotenv');
const path = require('path');

// Always load node/.env, even if the process is started from another folder.
// Use override so local .env is the source of truth during development.
dotenv.config({ path: path.join(__dirname, '.env'), override: true });

const {
  PORT,
  HOST,
  HOST_URL,
  API_KEY,
  AUTH_DOMAIN,
  PROJECT_ID,
  STORAGE_BUCKET,
  MESSAGING_SENDER_ID,
  APP_ID,
} = process.env;

module.exports = {
  port: PORT || 1000,
  host: HOST || 'localhost',
  url: HOST_URL || `http://${HOST || 'localhost'}:${PORT || 1000}`,
  firebaseConfig: {
    apiKey: API_KEY,
    authDomain: AUTH_DOMAIN,
    projectId: PROJECT_ID,
    storageBucket: STORAGE_BUCKET,
    messagingSenderId: MESSAGING_SENDER_ID,
    appId: APP_ID,
  },
};
