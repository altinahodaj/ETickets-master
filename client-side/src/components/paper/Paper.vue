<template>
  <b-card no-body :class="`paper ${paperClass}`">
    <b-card-header
      v-if="title || $slots.title"
      header-border-variant="light"
      header-class="border-default border-b"
      class="text-thicker text-md paper-header d-flex justify-content-between"
      :class="headerClass"
    >
      <slot name="title">
        <div class="paper-header-left d-flex align-items-center">
          <span>
            {{ title }}
          </span>
        </div>
      </slot>
      <div class="paper-header-right">
        <slot name="header-right" />
      </div>
    </b-card-header>

    <b-card-body :class="`${bodyClass} p-0 ${tabbed ? '' : 'mt-2'}`">
      <slot />
    </b-card-body>
  </b-card>
</template>

<script>
export default {
  name: "Paper",
  props: {
    title: {
      type: String,
      default: "",
    },
    paperClass: {
      type: String,
      default: "",
    },
    headerClass: {
      type: String,
      default: "",
    },
    bodyClass: {
      type: String,
      default: "",
    },
    tabbed: {
      type: Boolean,
      default: false,
    },
    info: {
      type: Object,
      default: null,
    },
  },
};
</script>

<style></style>
