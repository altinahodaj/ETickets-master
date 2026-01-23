"use strict";

const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const config = require("./config");
const mongoose = require("mongoose");

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

const port = 3000;
const server = app.listen(port, "0.0.0.0", () => {
  console.log("------------------------------------------");
  console.log("SERVER STARTING ON PORT " + port);
  console.log("Check http://localhost:" + port + "/api/health");
  console.log("------------------------------------------");
});

server.on('error', (err) => {
    console.error("SERVER ERROR:", err);
});

const connectionSting = "mongodb://localhost:27017/cinemaverse_db";
mongoose
  .connect(connectionSting)
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.log("MongoDB failed (optional)"));
