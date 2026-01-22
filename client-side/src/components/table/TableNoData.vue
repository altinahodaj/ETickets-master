<template>
  <div v-if="hasPermissions" class="no-data table-no-data">
    <div class="table-no-data-img">
      <icon v-if="customIcon" :name="customIcon" size="65" />
    </div>
    <span class="no-data__text">{{ noDataText }}</span>
    <div v-if="createText !== null">
      <a class="link cursor-pointer" @click="$emit('action')">{{
        createText
      }}</a>
    </div>
  </div>
  <div v-else class="no-data table-no-data">
    <b-img
      class="no-permissions"
      :src="require('@/assets/not-found.jpg')"
      alt="Error page"
    />
    <p>You don’t have permission to access {{ accessPage }} on this project.</p>
  </div>
</template>
<script>
import Icon from "@/components/Icon.vue";
import { BImg } from "bootstrap-vue";

export default {
  name: "TableNoData",
  components: { Icon, BImg },
  props: {
    noDataText: {
      type: String,
      default: null,
    },
    createText: {
      type: String,
      default: null,
    },
    icon: {
      type: String,
      default: "Globe",
    },
    hasPermissions: {
      type: Boolean,
      default: true,
    },
    accessPage: {
      type: String,
      default: "this page",
    },
    customIcon: {
      type: String,
      default: null,
    },
  },
};
</script>
<style lang="scss" scoped>
.no-permissions {
  max-width: 200px;
  margin: auto;
}
</style>
