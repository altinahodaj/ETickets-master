"use strict";

const admin = require("firebase-admin");
const path = require("path");
const fs = require("fs");

let app;

function getAdminApp() {
  if (app) return app;

  // Prefer a local service account file bundled with this project.
  // NOTE: This file is sensitive; keep it out of public repos.
  const serviceAccountPath = path.join(__dirname, "serviceAccountKey.json");
  if (!fs.existsSync(serviceAccountPath)) {
    throw new Error(
      `Missing ${serviceAccountPath}. Needed to set Firebase Auth custom claims (isAdmin).`
    );
  }

  // eslint-disable-next-line global-require, import/no-dynamic-require
  const serviceAccount = require(serviceAccountPath);

  app = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
  });

  return app;
}

function getAuth() {
  return getAdminApp().auth();
}

module.exports = {
  admin,
  getAdminApp,
  getAuth,
};
