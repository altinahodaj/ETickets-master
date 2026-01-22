import axios from "axios";

const token =
	"eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OTZmOTM5N2Y4YTBlMGM3NzU0MmRlNDQxMGQ3NzI3MiIsInN1YiI6IjYyYTQ4OTk4MDBiZmU4MDI1NTY5MDZlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZcJGq8Uqv2pwn0IOigDBGkLyNjiQiGj4WjQl42GVVNo";

export default axios.create({
	baseURL: "https://api.themoviedb.org/3",
	headers: {
		Authorization: `Bearer ${token}`,
	},
});
