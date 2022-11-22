<script setup>
import { ref } from "vue";
import CardDiscipline from "../components/CardDiscipline.vue";
import { URL } from "../config";

const disciplines = ref({});
const info = ref({});


//Recupera todas las disciplinas
(async () => {
  const res = await fetch(`${URL}/club/disciplines`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    }
  });

  const json = await res.json();
  disciplines.value = json;
  console.log(disciplines.value)
})();

//Recupera la información del club
(async () => {
  const res2 = await fetch(`${URL}/club/info`, {
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    }
  });

  const json2 = await res2.json();
  info.value = json2;
})();


</script>

<template>
  <header class="absolute top-0 left-0 bg-gray-800 w-full z-10">
    <img src="../assets/blob-haikei.svg" />
    <img
      src="../assets/gimp.png"
      class="absolute top-[72px] left-[100px] w-[600px]"
    />
    <div class="absolute right-[200px] top-1/3 flex flex-col items-center">
      <h1 class="text-6xl text-white font-semibold whitespace-nowrap bordeCss">
        Club Atletico Villa Elvira
      </h1>
      <span class="text-xl text-gray-500 font-semibold w-[600px] text-center">
        Frase corta y resumida que despierta emociones en la persona que la lea.
        Pueden ser dos oraciones, la verdad ni idea hay que charlarlo.
      </span>
    </div>
  </header>
  <section class="mt-[500px] p-10 w-screen h-auto">
    <article>
      <h1 class="text-4xl text-[#8D72E1] font-semibold whitespace-nowrap">
        Sobre nosotros
      </h1>
      <p class="mb-3 font-semibold text-gray-500 dark:text-gray-400">
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's standard dummy text ever
        since the 1500s, when an unknown printer took a galley of type and
        scrambled it to make a type specimen book. It has survived not only five
        centuries, but also the leap into electronic typesetting, remaining
        essentially unchanged. It was popularised in the 1960s with the release
        of Letraset sheets containing Lorem Ipsum passages, and more recently
        with desktop publishing software like Aldus PageMaker including versions
        of Lorem Ipsum.

      </p>
      <p class="mb-3 text-xl font-semibold text-gray-500 dark:text-gray-400"><span class="text-xl text-[#8D72E1] ">Email: </span>{{info.email}}</p>
      &nbsp;
      <p class="mb-3 text-xl font-semibold text-gray-500 dark:text-gray-400"><span class="text-xl text-[#8D72E1] ">Teléfono: </span>{{info.phone}}</p>

    </article>
    <article>
      <h1 class="text-4xl text-[#8D72E1] font-semibold whitespace-nowrap">
        Nuestras disciplinas
      </h1>
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-10 mt-10">
        <CardDiscipline
          v-for="discipline in disciplines"
          :name="discipline.nombre"
          :categoria="discipline.categoria.nombre"
          :id="discipline.id"
        ></CardDiscipline>
      </div>
    </article>
  </section>
</template>

<style>
.bordeCss{
  color: white;
  text-shadow:
   3px -1px 0 #000,  
    2px -1px 0 #000,
    -1px 1px 0 #000,
     4px 1px 0 #000;
}


</style>