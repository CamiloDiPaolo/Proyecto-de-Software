import { URL } from "../config";

export default async function auth() {
  try {
    const url = "http://127.0.0.1:5000/api";
    const res = await fetch(`${URL}/me/profile`, {
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-type": "application/json",
      },
      mode: "cors",
    });
    const data = await res.json();

    return data;
  } catch (err) {
    return {
      status: 401,
      err,
    };
  }
}
