import axios from "axios";

const getEvents = async () => {
  const apiCaller = axios.create({
    baseURL: "http://127.0.0.1:8000/",
  });
  const { data } = await apiCaller.get(`api/events/`);

  return data;
};

export default getEvents;
