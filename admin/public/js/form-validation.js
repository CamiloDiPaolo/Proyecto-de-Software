console.log("Vinculado")

const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/ // 7 a 14 numeros.
}

function addEmptyListener(field){
    field.addEventListener("blur", function(e) {
    const field = e.target;
    const divError = field.nextElementSibling.innerHTML
    if (field.value.length === 0){
        field.nextElementSibling.innerHTML = "El campo no puede estar vacío"; 
        return false;
    }
    else{
        field.nextElementSibling.innerHTML = ""; 
        return true;
    }
  })
}