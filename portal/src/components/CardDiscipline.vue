<script setup>

import { RouterView, RouterLink } from "vue-router";
import { URL } from "../config";
const props = defineProps(["name", "categoria","id"]);
const $url = URL;
const disciplineLink = "/discipline/" + props.id;
</script>

<template>
  <div
    class="p-6 max-w-sm bg-white rounded-lg border border-gray-200 dark:bg-gray-800 dark:border-gray-700 shadow-lg shadow-indigo-900 hover:pointer hover:shadow-xl hover:shadow-indigo-900 transition hover:-translate-y-1"
  >
      
  <RouterLink
            v-bind:to="disciplineLink"
            class="block py-2 pr-4 pl-3 text-gray-100 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-indigo-300 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >
      <h5
        class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white"
      >
        {{ props.name }}
      </h5>
  </RouterLink>
    <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">
      {{ props.categoria }}
    </p>
    
  <RouterLink
            v-bind:to="disciplineLink"
            class="block py-2 pr-4 pl-3 text-gray-100 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-indigo-300 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            > 

    <a
      
      class="inline-flex items-center text-indigo-600 hover:underline"
    >
      Averigua mas sobre esta disciplina!
      <svg
        class="ml-2 w-5 h-5"
        fill="currentColor"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"
        ></path>
        <path
          d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"
        ></path>
      </svg>
      </a>
  </RouterLink>

  </div>
</template>
