<template>
  <component :is="name" :size="size" />
</template>
<script>
export default {
  name: "LogoIcon",
  components: {},
  props: {
    name: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      default: "24",
    },
  },
};
</script>
