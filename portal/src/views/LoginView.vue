<script setup>
import { ref } from "vue";
import { URL } from "../config";

const username = ref("");
const password = ref("");

const login = async (e) => {
  e.preventDefault();
  try {
    const res = await fetch(`${URL}/auth`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });
    const data = await res.json();
    if (data.status != 401) location.href = "/";
  } catch (err) {
    console.log("algo salio mal con el login", err);
  }
};
</script>

<template>
  <form
    class="border-dashed border-4 border-indigo-500 p-10 rounded-lg"
    @submit.prevent="login"
  >
    <div class="mb-6">
      <label
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Numero de Socio</label
      >
      <input
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-500 dark:focus:border-indigo-500 outline-none"
        required
        v-model="username"
      />
    </div>
    <div class="mb-6">
      <label
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Contraseña</label
      >
      <input
        type="password"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-500 dark:focus:border-indigo-500 outline-none"
        required
        v-model="password"
      />
    </div>
    <button
      type="submit"
      class="text-white bg-indigo-700 hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm w-full px-5 py-2.5 text-center dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800"
    >
      Submit
    </button>
  </form>
</template>
