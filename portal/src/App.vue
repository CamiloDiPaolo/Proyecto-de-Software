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
      { name: 'pagina principal', to: '/' },
      { name: 'contacto', to: '/about' },
      { name: 'estadisticas', to: '/stats' },
      { name: 'Mis Pagos', to: '/payments' },
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
