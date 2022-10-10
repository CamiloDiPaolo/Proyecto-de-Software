"use stric";

const selectbtns = document.querySelectorAll("#select");

selectbtns.forEach((btn) =>
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    location.href = `/pagos/${btn.value}`;
  })
);
