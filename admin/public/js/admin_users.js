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

// TANTO AL CREAR COMO AL EDITAR UN USUARIO PARSEAMOS LOS ROLES EN UN ARREGLO
const form = document.querySelector(".admin__form--create");
form?.addEventListener("submit", async (e) => {
  const rolesDivs = [...e.target.querySelectorAll(".rol__added")];
  if (rolesDivs.length) {
    e.target.roles.value = JSON.stringify(
      rolesDivs.map((div) => div.dataset.id * 1)
    );
  } else {
    e.target.roles.value = "empty";
  }
  return true;
});

const formUpdate = document.querySelector(".admin__form--update");
formUpdate?.addEventListener("submit", async (e) => {
  const rolesDivs = [...e.target.querySelectorAll(".rol__added")];
  if (rolesDivs.length) {
    e.target.roles.value = JSON.stringify(
      rolesDivs.map((div) => div.dataset.id * 1)
    );
  } else {
    e.target.roles.value = "empty";
  }
  return true;
});
