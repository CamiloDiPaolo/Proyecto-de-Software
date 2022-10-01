// LOGICA PARA CREAR UN USUARIO
const form = document.querySelector(".admin__form--create");

form?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const inputs = [...e.target.querySelectorAll("input")];
  const data = {
    nombre: inputs[0].value,
    horarios: inputs[1].value,
    instructores: inputs[2].value,
    costo: inputs[3].value,
    habilitado: inputs[4].value,
    categoria_id: inputs[5].value
  };

  try {
    const res = await fetch(`http://${location.host}/disciplines/create`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (res.status == 200) location.href = "/admin/users";
  } catch (err) {
    console.log(err);
  }
});

// LOGICA PARA CMODIFICAR UN USUARIO
const formUpdate = document.querySelector(".admin__form--update");

formUpdate?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const inputs = [...e.target.querySelectorAll("input")];
  const rolesDivs = [...e.target.querySelectorAll(".rol__added")];
  const roles = rolesDivs.map((div) => div.dataset.id * 1);
  const data = {
    username: inputs[0].value,
    nombre: inputs[1].value,
    apellido: inputs[2].value,
    email: inputs[3].value,
    contraseña: inputs[4].value
  };
  console.log(data);
  try {
    const res = await fetch(
      `http://${location.host}/users/update/${location.href.split("/").at(-1)}`,
      {
        method: "PUT",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    if (res.status == 200) location.href = "/admin/users";
  } catch (err) {
    console.log(err);
  }
});
