const mongoose = require("mongoose");

// const schema = mongoose.Schema({
// 	reviews: String,
// 	film: String,
// 	client: String,
// });

class User {
	constructor(reviews, film, client) {
		this.reviews = reviews;
		this.film = film;
		this.client = client;
	}
}

const model = mongoose.model("reviews" + User);

module.exports = { model };

// module.exports = User;
