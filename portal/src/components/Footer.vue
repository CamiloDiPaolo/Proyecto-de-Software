<script>
export default {
  props: {
    phone: String,
    email: String
  }
}
</script>
<template>
  <footer
    class="p-4 bg-gray-900 grid grid-cols-2 shadow  md:flex md:flex-col md:justify-center dark:bg-gray-800"
  >
  <div class="grid grid-cols-2 xl:grid-cols-2 md:flex md:flex-col md:justify-center">
  
  <p class="text-white">Teléfono: {{phone}}</p>
  <p class="text-white">Email: {{email}}</p>
  
</div>
    <span class="text-sm text-gray-300 sm:text-center dark:text-gray-400"
      >Grupo 21 - Proyecto de software
    </span>


  </footer>
</template>
