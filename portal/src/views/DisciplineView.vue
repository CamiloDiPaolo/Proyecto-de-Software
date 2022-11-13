<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { URL } from "../config";
import router from "../router";

const route = useRoute();
const id = route.params.id;

const discipline = ref({});

(async () => {
  const res = await fetch(`${URL}/discipline/` + id, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });

  const json = await res.json();
  discipline.value = json;
  console.log(discipline.value);
})();
</script>
<template>
  <div class="flex flex-col gap-10">
    <h1 class="text-4xl text-[#8D72E1] font-semibold whitespace-nowrap">
      {{ discipline.nombre }}
    </h1>
    <div class="grid grid-cols-1 gap-10 xl:grid-cols-2">
      <div
        class="shadow-2xl flex flex-col p-10 border-2 border-gray-700 rounded-lg bg-gray-900 text-left content-start"
      >
        <p class="font-normal text-left text-gray-300 dark:text-gray-400">
          <span
            class="font-normal text-left text-[#8D72E1] text-gray-300 dark:text-gray-400"
            >Costo:</span
          >
          {{ discipline.costo }}
        </p>
        <p class="font-normal text-gray-300 dark:text-gray-400">
          <span
            class="font-normal text-[#8D72E1] text-gray-300 dark:text-gray-400"
            >Instructores:</span
          >
          {{ discipline.instructores }}
        </p>
        <p class="font-normal text-gray-300 dark:text-gray-400">
          <span
            class="font-normal text-[#8D72E1] text-gray-300 dark:text-gray-400"
            >Horarios:</span
          >
          {{ discipline.horarios }}
        </p>
        <p class="font-normal text-gray-300 dark:text-gray-400">
          <span
            class="font-normal text-[#8D72E1] text-gray-300 dark:text-gray-400"
            >Categoría:</span
          >
          {{ discipline.categoria.nombre }}
        </p>
        <br />
        &nbsp;
      </div>
    </div>
  </div>
</template>
