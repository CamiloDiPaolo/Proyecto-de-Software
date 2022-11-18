<script setup>
import { ref } from "vue";
import ChartPie from "../components/ChartPie.vue";
import ChartBar from "../components/ChartBar.vue";
import Spinner from "../components/Spinner.vue";
import { URL } from "../config";

// obtenemos los datos de las estadisticas
const loading1 = ref(true);
const data1 = ref({});

const loading2 = ref(true);
const data2 = ref({});

const loading3 = ref(true);
const data3 = ref({});

// cargamos los datos
(async () => {
  // cargamos los usuarios activos e inactivos
  const res = await fetch(`${URL}/socios/actives`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json = await res.json();
  data1.value = json;
  loading1.value = false;

  // cargamos la cantidad de socios con la cuota al dia
  const res2 = await fetch(`${URL}/socios/morosos`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json2 = await res2.json();
  data2.value = json2;
  console.log("------------------- MOROSOS -------------------");
  console.log(data2.value);
  loading2.value = false;

  // cargamos la cantidad de socios inscriptos a cada disciplina
  const res3 = await fetch(`${URL}/disciplines/cant`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json3 = await res3.json();
  data3.value.labels = json3.map((discipline) => discipline.name);
  data3.value.values = json3.map((discipline) => discipline.cant);
  console.log("------ DATA 3 ----");
  console.log(data3.value);
  loading3.value = false;
})();
</script>
<template>
  <div class="flex flex-col gap-10 w-2/3">
    <h1 class="text-4xl text-[#8D72E1] font-semibold whitespace-nowrap">
      Estadisticas
    </h1>
    <div class="grid grid-cols-1 gap-10 xl:grid-cols-2">
      <div
        class="shadow-2xl flex flex-col items-center p-10 border-2 border-gray-700 rounded-lg bg-gray-900"
      >
        <p class="font-normal text-gray-300 dark:text-gray-400">
          Cantidad de socios activos
        </p>
        <ChartPie
          :labels="['activos', 'inactivos']"
          :data="[data1.active, data1.inactive]"
          :colors="['#8D72E1', '#FF0066']"
          v-if="!loading1"
        ></ChartPie>
        <Spinner v-if="loading1"></Spinner>
      </div>

      <div
        class="shadow-2xl flex flex-col items-center p-10 border-2 border-gray-700 rounded-lg bg-gray-900"
      >
        <p class="font-normal text-gray-300 dark:text-gray-400">
          Cantidad de socios con la cuota al dia
        </p>
        <ChartPie
          :labels="['socios al dia', 'socios morosos']"
          :data="[data2.total - data2.morosos, data2.morosos]"
          :colors="['#8D72E1', '#FF0066']"
          v-if="!loading2"
        ></ChartPie>
        <Spinner v-if="loading2"></Spinner>
      </div>

      <div
        class="shadow-2xl flex flex-col items-center p-10 col-span-1 xl:col-span-2 w-full border-2 border-gray-700 rounded-lg bg-gray-900"
      >
        <p class="font-normal text-gray-300 dark:text-gray-400">
          Cantidad de socios inscriptos a cada disciplina
        </p>
        <ChartBar
          :labels="data3.labels"
          :data="data3.values"
          :colors="['#8D72E1', '#FF0066']"
          class="w-full"
          v-if="!loading3"
        ></ChartBar>
        <Spinner v-if="loading3"></Spinner>
      </div>
    </div>
  </div>
</template>
