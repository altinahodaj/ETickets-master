<template>
  <b-card
    no-body
    :class="`paper ${cardClass}`"
  >
    <b-card-body
      :class="`${bodyClass} paper-body`"
    >
      <slot />
    </b-card-body>
  </b-card>
</template>

<script>
export default {
  name: 'PaperSimple',
  props: {
    cardClass: {
      type: String,
      default: '',
    },
    bodyClass: {
      type: String,
      default: '',
    },
  },
}
</script>

<style>

</style>
