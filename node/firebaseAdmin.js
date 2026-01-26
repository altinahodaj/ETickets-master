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

  const expectedProjectId = String(process.env.PROJECT_ID || "").trim();
  const serviceAccountProjectId = String(serviceAccount?.project_id || "").trim();
  if (expectedProjectId && serviceAccountProjectId && expectedProjectId !== serviceAccountProjectId) {
    console.warn(
      "[firebase-admin] PROJECT_ID mismatch. ",
      `env PROJECT_ID='${expectedProjectId}' but serviceAccount project_id='${serviceAccountProjectId}'. ` +
        "Admin claims (isAdmin) will be set in the service account project, not the client project."
    );
  }

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
