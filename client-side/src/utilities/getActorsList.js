import axios from "axios";

const getActors = async () => {
  const apiCaller = axios.create({
    baseURL: "http://127.0.0.1:8000/",
  });
  const { data } = await apiCaller.get(`api/actors/`);

  return data;
};

export default getActors;
