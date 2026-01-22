"use strict";

const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const config = require("./config");
const mongoose = require("mongoose");

//ROUTES
const userRoutes = require("./Routes/user-routes");
// const ReviewRoute = require("./Routes/ReviewRoute");

const connectionSting = "mongodb://localhost:27017/cinemaverse_db";

const port = config.port || 1000;

const app = express();

app.use(express.json());
app.use(cors());
app.use(bodyParser.json());

// Health endpoint: helps verify runtime config (no secrets)
app.get("/api/health", (req, res) => {
  res.status(200).json({
    ok: true,
    firebase: {
      projectId: config?.firebaseConfig?.projectId || null,
      authDomain: config?.firebaseConfig?.authDomain || null,
    },
  });
});

app.use("/api", userRoutes.routes);
// app.use("/review", ReviewRoute.routes);

const startServer = () => {
  app.listen(port, () => {
    console.log("App is listening on url http://localhost:" + port);
  });
};

mongoose
  .connect(connectionSting)
  .then(() => {
    console.log("Connected to mongodb on: " + connectionSting);
    startServer();
  })
  .catch((err) => {
    console.warn(
      "MongoDB is not available (" + connectionSting + "). Starting API anyway."
    );
    console.warn(err?.message || err);
    startServer();
  });
