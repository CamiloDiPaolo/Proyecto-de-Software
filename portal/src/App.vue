<script setup>
import { RouterView } from "vue-router";
import { ref } from "vue";
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

const login = ref(false);
login.value = location.href.includes("login");
</script>

<template>
  <Navbar
    v-if="!login"
    :menus="[
      { name: 'Inicio', to: '/' },
      { name: 'Contacto', to: '/about' },
      { name: 'Estadisticas', to: '/stats' },
      { name: 'Mis Pagos', to: '/payments' },
      { name: 'Mi Cuenta', to: '/me' },
    ]"
  ></Navbar>

  <main
    :class="`${
      login ? ' ' : 'pt-16'
    } flex min-h-screen justify-center items-center w-screen pb-12 pt-32 z-40 bg-gray-800`"
  >
    <RouterView />
  </main>
  <Footer></Footer>
</template>
