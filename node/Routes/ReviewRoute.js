const express = require("express");
const ReviewController = require("../Controllers/ReviewController");

const ReviewRoute = express.Router();

ReviewRoute.get("/", ReviewController.list);

ReviewRoute.get("/:id", ReviewController.get);

ReviewRoute.post("/create", ReviewController.post);

ReviewRoute.put("/update/:id", ReviewController.put);

ReviewRoute.delete("/delete/:id", ReviewController.delete);

// module.exports = ReviewRoute;

module.exports = {
	routes: ReviewRoute,
};
