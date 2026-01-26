"use strict";

const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const config = require("./config");
const mongoose = require("mongoose");
const { getAuth } = require("./firebaseAdmin");

const app = express();
app.use(express.json());
app.use(cors());
app.use(bodyParser.json());

// LOG EVERY REQUEST
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    if (req.method === 'POST' || req.method === 'PUT') {
        console.log("Body:", JSON.stringify(req.body));
    }
    next();
});

// GLOBAL ERROR HANDLING
process.on("uncaughtException", (err) => {
    console.error("UNCAUGHT EXCEPTION:", err);
});
process.on("unhandledRejection", (reason, p) => {
    console.error("UNHANDLED REJECTION:", reason);
});

// Health endpoint
app.get("/api/health", (req, res) => {
  res.status(200).json({
    ok: true,
    firebase: {
      projectId: config?.firebaseConfig?.projectId || "unknown",
    },
  });
});

async function bootstrapAdminClaims() {
  const adminUids = String(process.env.ADMIN_UIDS || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const adminEmails = String(process.env.ADMIN_EMAILS || "")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);

  if (adminUids.length === 0 && adminEmails.length === 0) return;

  try {
    const auth = getAuth();

    for (const uid of adminUids) {
      try {
        await auth.setCustomUserClaims(String(uid), { isAdmin: true });
        console.log(`[bootstrap] ensured admin claim for UID ${uid}`);
      } catch (e) {
        console.warn(`[bootstrap] failed to set claim for UID ${uid}:`, e?.message || e);
      }
    }

    for (const email of adminEmails) {
      try {
        const user = await auth.getUserByEmail(String(email));
        await auth.setCustomUserClaims(String(user.uid), { isAdmin: true });
        console.log(`[bootstrap] ensured admin claim for email ${email} (uid ${user.uid})`);
      } catch (e) {
        console.warn(`[bootstrap] failed to set claim for email ${email}:`, e?.message || e);
      }
    }
  } catch (e) {
    console.warn("[bootstrap] admin claims bootstrap skipped:", e?.message || e);
  }
}

// Root route
app.get("/", (req, res) => {
  res.send("<h1>ETickets Node API</h1><p>Running on port 3000. Go to <a href='/api/users'>/api/users</a></p>");
});

// Import and use routes
try {
    const userRoutes = require("./Routes/user-routes");
    app.use("/api", userRoutes.routes);
} catch (err) {
    console.error("Error loading routes:", err);
}

const port = Number(config?.port) || 3000;
const server = app.listen(port, "0.0.0.0", () => {
  console.log("------------------------------------------");
  console.log("SERVER STARTING ON PORT " + port);
  console.log("Check http://localhost:" + port + "/api/health");
  console.log("------------------------------------------");

  // Ensure configured admins always have the Auth claim
  bootstrapAdminClaims();
});

server.on('error', (err) => {
    console.error("SERVER ERROR:", err);
});

const connectionSting = "mongodb://localhost:27017/cinemaverse_db";
mongoose
  .connect(connectionSting)
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.log("MongoDB failed (optional)"));
