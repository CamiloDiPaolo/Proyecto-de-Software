<script setup>
import { RouterView } from "vue-router";
import { ref } from "vue";
import auth from "./router/middleware/auth";
import Navbar from "./components/Navbar.vue";
import { URL } from "./config";
import Footer from "./components/Footer.vue";

const login = ref(false);
const logged = ref(false);

login.value = location.href.includes("login");
(async () => {
  const res = await auth();
  logged.value = res.status !== 401;
})();
const info = ref({});

//Recupera la información del club
(async () => {
  const res2 = await fetch(`${URL}/club/info`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    }
  });

  const json2 = await res2.json();
  info.value = json2;
})();
</script>

<template>
  <Navbar
    v-if="!login && !logged"
    :menus="[
      { name: 'Inicio', to: '/' },
      { name: 'Estadisticas', to: '/stats' },
      { name: 'Iniciar Sesion', to: '/login' },
    ]"
  ></Navbar>
  <Navbar
    v-if="!login && logged"
    :menus="[
      { name: 'Inicio', to: '/' },
      { name: 'Estadisticas', to: '/stats' },
      { name: 'Mis Pagos', to: '/payments' },
      { name: 'Mi Cuenta', to: '/me' },
      { name: 'Cerrar Sesion', to: '/logout' },
    ]"
  ></Navbar>

  <main
    :class="`${
      login ? ' ' : 'pt-16'
    } flex min-h-screen justify-center items-center w-screen pb-12 pt-32 z-40 bg-gray-800`"
  >
    <RouterView />
  </main>
  <Footer
    :phone=info.phone
    :email=info.email
  ></Footer>
</template>
