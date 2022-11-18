<script setup>
import { BarChart } from "vue-chart-3";
import Chart from "chart.js/auto";

const props = defineProps(["labels", "data", "colors", "title"]);
console.log(" --- PROPS --- ");
console.log(props.labels);
console.log(props.data);
console.log(props.colors);
console.log(props.title);
</script>

<template>
  <BarChart
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
