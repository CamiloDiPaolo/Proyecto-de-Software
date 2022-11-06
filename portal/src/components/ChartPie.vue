<script setup>
import { DoughnutChart } from "vue-chart-3";
import Chart from "chart.js/auto";

const props = defineProps(["labels", "data", "colors"]);
console.log(props);
</script>

<template>
  <DoughnutChart
    :chartData="{
      labels: props.labels,
      datasets: [
        {
          data: props.data,
          backgroundColor: props.colors,
        },
      ],
    }"
    class="w-96 h-96"
  />
</template>
