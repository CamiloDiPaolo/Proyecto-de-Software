import { URL } from "../../config";

export default async function auth() {
  try {
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
