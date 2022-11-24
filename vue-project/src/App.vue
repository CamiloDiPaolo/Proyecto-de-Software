<script setup>
import { RouterView } from "vue-router";
import { ref } from "vue";
import Navbar from "./components/Navbar.vue";

const login = ref(false);
login.value = location.href.includes("login");
</script>

<template>
  <Navbar
    v-if="!login"
    :menus="[
      { name: 'home', to: '/' },
    ]"
    :userOptions="[
      { name: 'Perfil', to: '/' },
      { name: 'Salir', to: '/' },
    ]"
  ></Navbar>

  <main
    :class="`${
      login ? ' ' : 'pt-16'
    } flex min-h-screen justify-center items-center`"
  >
    <RouterView />
  </main>
</template>
