<template>
  <div
    class="select-button"
    @click="$emit('click')"
  >
    <template v-if="selected">
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect
          x="3"
          y="3"
          width="18"
          height="18"
          rx="4"
          fill="#1D79F2"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M16.807 7.92101C16.9887 8.09059 16.9985 8.37534 16.829 8.55703L9.88379 15.9983C9.67624 16.2207 9.32374 16.2207 9.11619 15.9983L7.17101 13.9142C7.00144 13.7325 7.01126 13.4477 7.19295 13.2782C7.37463 13.1086 7.65939 13.1184 7.82896 13.3001L9.49999 15.0905L16.171 7.94295C16.3406 7.76126 16.6253 7.75144 16.807 7.92101Z"
          fill="white"
          stroke="white"
          stroke-width="0.4"
          stroke-linecap="round"
        />
      </svg>
      <span class="sr-only">Selected</span>
    </template>
    <template v-else>
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect
          x="3.7"
          y="3.7"
          width="16.6"
          height="16.6"
          rx="3.3"
          stroke="#A3B0C2"
          stroke-width="1.4"
        />
      </svg>
      <span class="sr-only">Not selected</span>
    </template>
  </div>
</template>
<script>
export default {
  name: 'SelectButton',
  props: {
    selected: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
