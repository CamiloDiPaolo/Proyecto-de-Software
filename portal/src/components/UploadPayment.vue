<script setup>
import { ref } from "vue";
import { URL } from "../config";

const pay = ref(0);
const date = ref(null);
const file = ref(null);
const error = ref(false);
const messageError = ref("");

const emit = defineEmits(["close"]);

const setFile = (e) => {
  e.preventDefault();
  file.value = e.target.files;
};

const validateExtensions = (name) => {
  const extensions = [".jpg", ".png", ".pdf"];
  return extensions.some((str) => name.toLowerCase().endsWith(str));
};

const upload = async (e) => {
  e.preventDefault();
  if (!validateExtensions(file.value[0].name)) {
    error.value = true;
    messageError.value = "Solo se permiten archivos tipo .png, .pdf y .jpg";
    return;
  }
  try {
    const res = await fetch(`${URL}/me/payments`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        pay: pay.value,
        date: date.value,
        certificate: file.value[0].name,
      }),
      mode: "cors",
    });
    const data = await res.json();
    if (data.status != 401 && data.status != 400) {
      error.value = false;
      emit("close");
    } else {
      error.value = true;
      messageError.value = data.message;
    }
  } catch (err) {
    error.value = true;
    messageError.value = err;
  }
};
</script>
<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  />
  <div
    class="fixed top-0 left-0 w-screen h-screen bg-gray-500 opacity-75"
  ></div>
  <div
    tabindex="-1"
    class="fixed top-1/4 left-1/2 z-50 h-modal w-96 h-40 transform -translate-x-1/2 -translate-y-1/2"
  >
    <div class="relative p-1 h-full md:h-auto">
      <div
        class="relative bg-gray-800 rounded-lg shadow p-10 border-4 border-indigo-500"
      >
        <form @submit.prevent="upload">
          <div class="mb-6">
            <label class="block mb-2 text-base font-medium text-black-900"
              >Monto:
            </label>
            <input
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600"
              type="number"
              required
              placeholder="Ingrense el Monto de la factura..."
              v-model="pay"
            />
          </div>
          <div class="mb-6">
            <label class="block mb-2 text-base font-medium text-black-900"
              >Fecha:
            </label>
            <input
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
              type="date"
              required
              v-model="date"
            />
          </div>
          <div class="mb-6">
            <label class="block mb-2 text-base font-medium text-black-900"
              >Certificado de Pago:
            </label>
            <input
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600"
              type="file"
              accept=".png,.pdf,.jpg"
              required
              v-on:change="setFile"
            />
          </div>
          <button
            class="text-white bg-indigo-700 hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm w-full px-5 py-2.5 text-center dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800"
            type="submit"
          >
            Subir Pago
          </button>
        </form>
        <div v-if="error" class="mt-6">
          <div
            class="block text-red-600 mb-2 text-lg font-medium flex justify-center"
          >
            <span class="material-symbols-outlined"> error</span>
          </div>
          <div
            class="block text-red-600 mb-2 text-base font-medium flex justify-center"
          >
            <span>{{ messageError }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
