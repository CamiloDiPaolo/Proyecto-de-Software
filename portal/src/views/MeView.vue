<script setup>
import { ref } from "vue";
import { URL } from "../config";

let info = ref({});

let disciplines = ref({});

(async () => {
  const res = await fetch(`${URL}/socios/infoCarnet`, {
    credentials: "include",
    mode:"cors",
    headers: {
      "Content-type": "application/json",
    },
  });

  const res2 = await fetch(`${URL}/me/disciplines`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });

  const json = await res.json();

  const json2 = await res2.json();


  //   payments.value = json;
  info.value = json;

  disciplines.value = json2;

})();
</script>
<template>
  <div class="flex flex-col gap-5">
    <div
      class="shadow-2xl flex flex-col p-10 border-2 border-gray-700 rounded-lg bg-gray-900"
    >
      <h1 class="text-4xl text-[#8D72E1] font-semibold whitespace-nowrap mb-8">
        Informacion Personal
      </h1>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Nombre y Apellido: </span>
        <span> {{ info.Nombre }} {{ info.Apellido }}</span>
      </div>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Tipo y Nro de Documento: </span>
        <span>{{ info.Tipo_Documento }} {{ info.Nro_Documento }}</span>
      </div>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Direccion: </span>
        <span> {{ info.Direccion }}</span>
      </div>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Genero: </span>
        <span> {{ info.Genero }}</span>
      </div>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Estado: </span>
        <span> {{ info.Estado }}</span>
      </div>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Email: </span>
        <span v-if="info.Email"> {{ info.Email }}</span>
        <span v-else> Sin Espeficicar</span>
      </div>
      <div class="font-normal text-gray-300 dark:text-gray-400 mb-2">
        <span class="font-semibold">Telefono: </span>
        <span v-if="info.Telefono"> {{ info.Telefono }}</span>
        <span v-else> Sin Espeficicar</span>
      </div>
    </div>
    <div
      class="shadow-2xl flex flex-col p-10 border-2 border-gray-700 rounded-lg bg-gray-900"
    >
      <h1 class="text-4xl text-[#8D72E1] font-semibold whitespace-nowrap mb-8">
        Disciplinas Inscriptas
      </h1>
      <ul>
      <div  v-for="discipline in disciplines">
        <li class="font-normal text-gray-300 dark:text-gray-400 mb-2"><span class="font-semibold">{{discipline.nombre}}</span>({{discipline.categoria.nombre}})</li>
      </div>
      </ul>
    </div>
  </div>
</template>
