<script setup>
const props = defineProps(["foo"]);
console.log(props);
</script>

<template>
  <p class="text-rose-500">hol q tal con tailwind {{ props.foo }}</p>
</template>
