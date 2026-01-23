<template>
  <b-card
    no-body
    class="overflow-hidden mx-auto"
    style="max-width: 540px; margin: 50px"
  >
    <b-row no-gutters>
      <b-card-img
        v-if="event.photos && event.photos.length > 0"
        :src="event.photos[0].imgClientPath"
        alt="Image"
      />
      <b-card-img
        v-else
        src="/assets/app_files/Movies/default-image.jpg"
        alt="Default Image"
      />
      <b-col md="6" class="text-center mx-auto">
        <b-card-body :title="event.name">
          <b-card-text>
            {{ event.description }}
          </b-card-text>
          <b-card-text> <b> Price: </b>{{ event.price }}€ </b-card-text>
          <b-card-text>
            {{ event.date }}
          </b-card-text>
          <b-button @click="onDetailsClick(event.id)" variant="primary"
            >Details</b-button
          >
        </b-card-body>
      </b-col>
    </b-row>
  </b-card>
</template>

<script>
export default {
  components: {},
  props: {
    event: Object,
  },
  computed: {
    events() {
      return this.$store.state.events.events;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
  },
  methods: {
    removeEvent(eventId) {
      this.$store.dispatch("removeEvent", eventId).then(() => {
        window.location.reload();
      });
    },
    onDetailsClick(eventId) {
      this.$router.push({
        name: "Event",
        params: { eventId: eventId },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
</style>
