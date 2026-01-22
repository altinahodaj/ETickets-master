<template>
  <b-button v-bind="{ ...$props, ...$attrs }" @click="$emit('click')">
    <b-spinner v-if="spinning" class="position-absolute" small />
    <span :class="{ unvisible: spinning }">
      <slot />
    </span>
  </b-button>
</template>
<script>
export default {
  props: {
    spinning: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
<style lang="scss" scoped>
.unvisible {
  visibility: hidden;
}
</style>
