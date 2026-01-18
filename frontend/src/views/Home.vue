<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-4">{{ title }}</h1>
    <p class="text-gray-600">Esta sección está en construcción.</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  title?: string;
}>();

const title = ref(props.title || "Página");
</script>
