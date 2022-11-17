<script setup>
import { ref } from "vue";
import { URL } from "../config";
import UploadPayment from "../components/UploadPayment.vue";

let upload = ref(false);

const payments = ref([]);
const monthsNames = [
  "Enero",
  "Febrero",
  "Marzo",
  "Abril",
  "Mayo",
  "Junio",
  "Julio",
  "Agosto",
  "Septiembre",
  "Octubre",
  "Noviembre",
  "Diciembre",
];

const getAllMonthsPayments = (payments) => {
  const allPayments = [];
  const months = {
    Jan: 0,
    Feb: 1,
    Mar: 2,
    Apr: 3,
    May: 4,
    Jun: 5,
    Jul: 6,
    Aug: 7,
    Sep: 8,
    Oct: 9,
    Nov: 10,
    Dec: 11,
  };
  payments.forEach((payment) => {
    const day = payment.fecha.split(" ")[1];
    const month = months[payment.fecha.split(" ")[2]];
    const year = payment.fecha.split(" ")[3];

    allPayments[months[payment.fecha.split(" ")[2]]] = payment;
    allPayments[
      months[payment.fecha.split(" ")[2]]
    ].fecha = `${day}/${month}/${year}`;
  });
  if (allPayments.length != 12) allPayments[11] = null;

  console.log(allPayments);
  return allPayments;
};

const closeAndReload = () => {
  upload = false;
  location.reload();
};

(async () => {
  const res = await fetch(`${URL}/me/payments`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  });
  const json = await res.json();
  //   payments.value = json;
  payments.value = getAllMonthsPayments(json);
  console.log(payments.value);
})();
</script>
<template>
  <div class="flex flex-col gap-10">
    <div class="flex justify-between">
      <span class="text-4xl text-[#8D72E1] font-semibold">
        Cuotas del Año Vigente
      </span>
      <button
        class="relative inline-flex items-center justify-center p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800"
        v-on:click="upload = true"
      >
        <span
          class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0"
        >
          Subir Compobante
        </span>
      </button>
    </div>

    <div class="grid grid-cols-4 gap-10 xl:grid-cols-4">
      <div
        class="shadow-2xl flex flex-col p-10 border-2 border-gray-700 rounded-lg bg-gray-900 text-left content-start"
        v-for="(index, key, value) in payments"
      >
        <div v-if="index">
          <p
            class="text-2xl font-semiblod text-center text-[#5433b8] dark:text-gray-400"
          >
            {{ monthsNames[key] }}
          </p>
          <p class="font-normal text-left text-gray-300 dark:text-gray-400">
            <span
              class="font-normal text-left text-[#8D72E1] text-gray-300 dark:text-gray-400"
              >Pago:</span
            >
            {{ index.pago }}
          </p>
          <p class="font-normal text-gray-300 dark:text-gray-400">
            <span
              class="font-normal text-[#8D72E1] text-gray-300 dark:text-gray-400"
              >Fecha:</span
            >
            {{ index.fecha }}
          </p>
          &nbsp;
        </div>
        <div v-else>
          <p
            class="text-2xl font-semiblod text-center text-[#5433b8] dark:text-gray-400"
          >
            {{ monthsNames[key] }}
          </p>
          <p class="font-normal text-red-300 dark:text-red-400">
            Pago sin realizar
          </p>
          &nbsp;
        </div>
      </div>
    </div>
  </div>
  <div v-if="upload">
    <UploadPayment @close="closeAndReload"> </UploadPayment>
  </div>
</template>
