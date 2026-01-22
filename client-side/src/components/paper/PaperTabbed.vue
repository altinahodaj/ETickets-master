<template>

  <paper
    :title="title"
    :header-class="headerClass"
    :body-class="`mt-0 ${bodyClass}`"
    :info="info"
    tabbed
  >
    <template v-slot:header-right>
      <slot name="header-right" />
    </template>
    <b-tabs
      v-model="value"
      card
      nav-class="m-0 paper-nav w-100 testing"
      nav-wrapper-class="px-0 paper-nav-wrapper border-default border-b"
      @input="(e)=>$emit('tabChanged', e)"
    >
      <slot />
    </b-tabs>
  </paper>

</template>

<script>
import Paper from './Paper.vue'

export default {
  name: 'PaperTabbed',
  components: { Paper },
  props: {
    title: {
      type: String,
      default: '',
    },
    headerClass: {
      type: String,
      default: '',

    },
    bodyClass: {
      type: String,
      default: '',
    },
    info: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      value: null,
    }
  },
}
</script>

<style>

</style>
