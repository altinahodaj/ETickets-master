import axios from "axios";

const getMovies = async () => {
  const apiCaller = axios.create({
    baseURL: "http://127.0.0.1:8000/",
  });
  const { data } = await apiCaller.get(`api/movies/`);

  return data;
};

export default getMovies;
