<template>
  <div>
    <div class="row">
      <div class="card" style="width: 15rem">
        <img
          v-if="event.photos && event.photos.length > 0"
          class="card-img-top"
          :src="event.photos[0].imgClientPath"
          alt="Card image cap"
        />
        <img
          v-else
          class="card-img-top"
          src="/assets/app_files/Movies/default-image.jpg"
          alt="Default image"
        />
        <h2 class="d-flex justify-content-center">{{ event.name }}</h2>
        <h6 class="d-flex justify-content-center">{{ event.price }}€</h6>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    event: {
      type: Object,
    },
  },
};
</script>
