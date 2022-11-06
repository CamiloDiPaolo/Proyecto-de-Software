<script setup>
import { UserCircleIcon } from "@heroicons/vue/20/solid/index.js";
import { RouterLink } from "vue-router";
import { ref } from "vue";

const props = defineProps(["menus", "userOptions"]);

const showUserData = ref(false);
const showNavResponsive = ref(false);
</script>

<template>
  <nav class="bg-gray-800 fixed left-0 w-screen z-50">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <!-- Mobile menu button-->
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            aria-controls="mobile-menu"
            aria-expanded="false"
            @click="
              () => {
                showNavResponsive = !showNavResponsive;
              }
            "
          >
            <svg
              class="block h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
              />
            </svg>
          </button>
        </div>
        <div
          class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start"
        >
          <div class="hidden sm:ml-6 sm:block">
            <div class="flex space-x-4">
              <RouterLink
                v-for="menu in props.menus"
                :to="menu.to"
                class="bg-gray-900 text-white px-3 py-2 rounded-md text-sm font-medium"
                >{{ menu.name }}</RouterLink
              >
            </div>
          </div>
        </div>
        <div
          class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0"
        >
          <!-- Profile dropdown -->
          <div class="relative ml-3">
            <div>
              <button
                class="flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                @click="
                  () => {
                    showUserData = !showUserData;
                  }
                "
              >
                <span class="sr-only">Open user menu</span>
                <UserCircleIcon class="h-10 text-gray-50"></UserCircleIcon>
              </button>
            </div>
            <div
              class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              v-if="showUserData"
            >
              <RouterLink
                v-for="menu in props.userOptions"
                :to="menu.to"
                class="block px-4 py-2 text-sm text-gray-700"
                >{{ menu.name }}</RouterLink
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile menu, show/hide based on menu state. -->
    <div class="sm:hidden" id="mobile-menu" v-if="showNavResponsive">
      <div class="space-y-1 px-2 pt-2 pb-3">
        <RouterLink
          v-for="menu in props.menus"
          :to="menu.to"
          class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >{{ menu.name }}</RouterLink
        >
      </div>
    </div>
  </nav>
</template>
