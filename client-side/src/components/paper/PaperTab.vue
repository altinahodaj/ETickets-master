<template>
  <b-tab
    :title="title"
    :active="active"
    title-link-class="paper-tabbed-link"
    no-body
  >
    <slot />
  </b-tab>
</template>

<script>
export default {
  name: 'PaperTab',
  props: {
    title: {
      type: String,
      default: '',
    },
    active: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style>

</style>
