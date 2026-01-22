<template>
  <b-dropdown
    :id="id"
    :text="displayText"
    variant="dropdown"
    :class="`
      dropdown-icon-wrapper
       ${sizeClass}
       ${wrapperClass}
       ${stateClass}
       `"
    :menu-class="`shadow-sm mt-0 ${sizeClass}`"
    toggle-class="w-100"
    offset="0"
    :disabled="disabled"
  >
    <template #button-content>
      <div class="d-flex justify-content-between align-items-center w-100">
        <div class="d-flex flex-column w-100 align-items-start">
          <span
            :class="`text-md mw-100 text-truncate lh-normal ${textColorClass}`"
          >
            {{ displayText }}
          </span>
          <span
            v-if="selectedItemDescription"
            class="text-xsm text-secondary mw-100 text-truncate lh-normal"
          >
            {{ selectedItemDescription }}
          </span>
        </div>
      </div>
    </template>
    <b-dropdown-item
      v-for="option in options"
      :key="getKey(option.value)"
      :disabled="selectable ? !selectable(option) : false"
      @click="onSelect(option.value)"
    >
      <div class="d-flex flex-column w-100">
        <div class="w-100" style="white-space: normal">
          {{ option.text }}
        </div>
        <div
          v-if="option.description"
          class="w-100 text-xsm text-secondary"
          style="white-space: normal"
        >
          {{ option.description }}
        </div>
      </div>
    </b-dropdown-item>
  </b-dropdown>
</template>

<script>
export default {
  name: "CustomSelect",
  props: {
    state: {
      default: true,
      type: Boolean,
    },
    size: {
      default: null,
      type: String,
    },
    selectable: {
      default: null,
      type: Function,
    },
    id: {
      default: null,
      type: [String, Number],
    },
    wrapperClass: {
      default: null,
      type: String,
    },
    disabled: {
      default: false,
      type: Boolean,
    },
    placeholder: {
      default: null,
      type: String,
    },
    options: {
      default: () => [],
      required: true,
      type: Array,
    },
    // eslint-disable-next-line vue/require-default-prop
    value: null,
  },
  computed: {
    selectedItem() {
      return this.options.find((option) => option.value === this.value);
    },
    displayText() {
      return this.selectedItem ? this.selectedItem.text : this.placeholder;
    },
    selectedItemDescription() {
      return this.selectedItem ? this.selectedItem.description || null : null;
    },
    stateClass() {
      if (this.size == null) return "";
      return this.state ? "" : "border-danger";
    },
    textColorClass() {
      return this.selectedItem ? "" : "text-secondary";
    },
    sizeClass() {
      return this.size === "auto" ? "" : "w-100";
    },
  },
  watch: {
    value(value) {
      this.$emit("change", value);
    },
  },
  methods: {
    getKey(value) {
      if (typeof value === "object") {
        return JSON.stringify(value);
      }
      return value;
    },
    onSelect(value) {
      this.$emit("input", value);
    },
  },
};
</script>

<style lang="scss" scoped>
.lh-normal {
  line-height: normal;
}
</style>
