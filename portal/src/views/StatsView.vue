<script setup>
import { ref } from "vue";
import ChartPie from "../components/ChartPie.vue";
import ChartBar from "../components/ChartBar.vue";
import Spinner from "../components/Spinner.vue";

// obtenemos los datos de las estadisticas
const loading1 = ref(true);
const data1 = ref({});

const loading2 = ref(true);
const data2 = ref({});

const loading3 = ref(true);
const data3 = ref({});

// cargamos los datos
(async () => {
  const url = "http://127.0.0.1:5000/api";

  // cargamos los usuarios activos e inactivos
  const res = await fetch(`${url}/socios/actives`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json = await res.json();
  data1.value = json;
  loading1.value = false;

  // cargamos la cantidad de socios con la cuota al dia
  const res2 = await fetch(`${url}/socios/morosos`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json2 = await res2.json();
  data2.value = json2;
  loading2.value = false;

  // cargamos la cantidad de socios inscriptos a cada disciplina
  const res3 = await fetch(`${url}/disciplines/cant`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json3 = await res3.json();
  data3.value.labels = json3.map((discipline) => discipline.name);
  data3.value.values = json3.map((discipline) => discipline.cant);
  console.log(data3.value);
  loading3.value = false;
})();
</script>
<template>
  <!-- <p>
    Graficos a mostrar: Cantidad de usuarios registrados a cada disciplina
    (Barra), Cantidad de usuarios al dia con la cuota(Torta), Cantidad de socios
    activos e inactivos(Torta)
  </p> -->
  <div class="flex flex-col gap-10 w-2/3">
    <h2
      class="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight"
    >
      Estadisticas
    </h2>
    <div class="grid grid-cols-1 gap-10 xl:grid-cols-2">
      <div
        class="shadow-2xl flex flex-col items-center p-10 border-2 border-gray-300 rounded-lg"
      >
        <p class="font-normal text-gray-700 dark:text-gray-400">
          Cantidad de socios activos
        </p>
        <ChartPie
          :labels="['activos', 'inactivos']"
          :data="[data1.active, data1.inactive]"
          :colors="['#232323', '#456756']"
          v-if="!loading1"
        ></ChartPie>
        <Spinner v-if="loading1"></Spinner>
      </div>

      <div
        class="shadow-2xl flex flex-col items-center p-10 border-2 border-gray-300 rounded-lg"
      >
        <p class="font-normal text-gray-700 dark:text-gray-400">
          Cantidad de socios con la cuota al dia
        </p>
        <ChartPie
          :labels="['socios al dia', 'socios morosos']"
          :data="[data2.total - data2.morosos, data2.morosos]"
          :colors="['#232323', '#456756']"
          v-if="!loading2"
        ></ChartPie>
        <Spinner v-if="loading2"></Spinner>
      </div>

      <div
        class="shadow-2xl flex flex-col items-center p-10 col-span-1 xl:col-span-2 w-full border-2 border-gray-300 rounded-lg"
      >
        <p class="font-normal text-gray-700 dark:text-gray-400">
          Cantidad de socios inscriptos a cada disciplina
        </p>
        <ChartBar
          :labels="data3.labels"
          :data="data3.values"
          :colors="['#232323', '#456756']"
          class="w-full"
          v-if="!loading3"
        ></ChartBar>
        <Spinner v-if="loading3"></Spinner>
      </div>
    </div>
  </div>
</template>
