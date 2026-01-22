<template>
  <div>
    <h1 class="container d-flex justify-content-center">Events</h1>
    <br />
    <hr />
    <div class="row">
      <Card v-for="entry in events" :key="entry.id" :event="entry" />
    </div>
  </div>
</template>

<script>
import Card from "../../components/Card.vue";

export default {
  name: "events",
  components: {
    Card,
  },
  data() {
    return {
      cinemaId: null,
    };
  },
  watch: {
    cinema() {
      return this.getEvents();
    },
  },
  computed: {
    loading() {
      return this.$store.state.events.loading;
    },
    events() {
      return this.$store.state.events.events;
    },
    cinema() {
      return this.$store.state.cinemas.cinema;
    },
  },
  created() {
    this.cinemaId = this.$route.params.cinemaId;
    this.getEvents();
  },
  methods: {
    getEvents() {
      this.$store
        .dispatch(
          "getEvents",
          this.cinemaId == null ? this.cinema.id : this.cinemaId
        )
        .then(() => {
          if (this.events.length > 0) {
            if (this.events.photos.length > 0) {
              this.events.photos.forEach((photo) => {
                require(photo.imgClientPath);
              });
            }
          }
        })
        .catch((error) => {
          console.log(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching events!"
          );
        });
    },
  },
};
</script>

<style lang="scss" scoped>
input {
  border: 1px solid black;
  padding: 20px;
  margin-top: 2%;
  margin-bottom: 2%;
  border-radius: 15px;
}
.row > * {
  flex-shrink: 0;
  width: 100%;
  max-width: 100%;
  padding-right: calc(var(--bs-gutter-x) * 0.5);
  padding-left: calc(var(--bs-gutter-x) * 0.5);
  margin-top: var(--bs-gutter-y);
}
</style>
