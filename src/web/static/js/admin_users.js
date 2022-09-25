// LOGICA PARA AGREGAR ROLES DE FORMA DINAMICA
const addRoleBtn = document.querySelector(".add__role");
const addRoleSelect = document.querySelector(".roles__input select");
const addedsRoles = document.querySelector(".roles__added");

addRoleBtn.addEventListener("click", (e) => {
  e.preventDefault();
  const divsRoles = [...addedsRoles.querySelectorAll("div")];
  if (!addRoleSelect.value) return;
  if (divsRoles.some((div) => div.dataset.id == addRoleSelect.value)) return;

  const div = document.createElement("div");
  const span = document.createElement("span");
  const icon = document.createElement("span");
  const btn = document.createElement("button");

  icon.classList.add("material-symbols-outlined");
  icon.textContent = "delete";

  btn.classList.add("delete__btn");
  btn.classList.add("action__btn");
  btn.appendChild(icon);

  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const divsRoles = [...addedsRoles.querySelectorAll("div")];
    divsRoles.forEach((div) => {
      if (div.dataset.id != addRoleSelect.value) return;
      addedsRoles.removeChild(div);
    });
  });

  span.textContent = addRoleSelect.querySelector("option:checked").textContent;

  div.dataset.id = addRoleSelect.value;
  div.classList.add("rol__added");
  div.appendChild(span);
  div.appendChild(btn);
  addedsRoles.appendChild(div);
});

// AGREGAMOS LAS FUNCIONES A LOS ROLES DEL USUARIO SELECCIONADO (FORM UPDATE)
[...document.querySelectorAll(".delete__btn")].forEach((btnDelete) => {
  btnDelete.addEventListener("click", (e) => {
    addedsRoles.removeChild(btnDelete.parentElement);
  });
});

// LOGICA PARA CREAR UN USUARIO
const form = document.querySelector(".admin__form--create");

form?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const inputs = [...e.target.querySelectorAll("input")];
  const rolesDivs = [...e.target.querySelectorAll(".rol__added")];
  const roles = rolesDivs.map((div) => div.dataset.id * 1);
  const data = {
    username: inputs[0].value,
    nombre: inputs[1].value,
    apellido: inputs[2].value,
    email: inputs[3].value,
    contraseña: inputs[4].value,
    activo: true,
    roles,
  };

  try {
    const res = await fetch(`http://${location.host}/users/create`, {
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
    contraseña: inputs[4].value,
    activo: true,
    roles,
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
