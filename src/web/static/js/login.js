const formLogin = document.querySelector(".form__login");

formLogin.addEventListener("submit", async (e) => {
  e.preventDefault();
  const inputs = [...e.target.querySelectorAll("input")];
  const user = {
    username: inputs[0].value,
    password: inputs[1].value,
  };

  try {
    const res = await fetch(`http://${location.host}/auth/login`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    });

    if (res.status == 200) location.href = "/admin";
  } catch (err) {
    console.log(err);
  }
});
