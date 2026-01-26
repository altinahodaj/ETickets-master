<template>
  <v-container class="mt-5">
    <h1 class="mb-6">Events</h1>

    <div v-if="loading">Loading...</div>

    <v-row v-else>
      <v-col cols="12" md="6" lg="4" v-for="e in events" :key="e.id">
        <v-card elevation="2" class="pa-2">
            <v-img
                :src="getEventImage(e)"
                height="260"
                contain
                class="event-poster"
                @error="onImgError(e)"
            />

          <v-card-title>{{ e.title }}</v-card-title>
          <v-card-text>
            <div class="mb-2">{{ e.description }}</div>
            <div class="grey--text">
              {{ formatDate(e.eventDate || e.event_date) }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "EventsList",
  computed: {
    loading() {
      return this.$store.state.events.loading;
    },
    events() {
      return this.$store.state.events.events || [];
    },
    cinemaId() {
      return this.$store.state.cinemas?.cinema?.id || 1;
    },
  },
  created() {
    this.$store.dispatch("getEventsByCinema", this.cinemaId);
  },
  methods: {
  formatDate(d) {
    if (!d) return "";
    return new Date(d).toLocaleString();
  },

  // ✅ Kjo e kthen URL-n e saktë gjithmonë
  getEventImage(e) {
    const base = "http://127.0.0.1:8000";

    // 1) nëse backend e kthen direkt URL
    if (e?.imgClientPath) return e.imgClientPath;
    if (e?.imageClientPath) return e.imageClientPath;

    // 2) nëse backend e kthen "app_files/Events/xxx.png"
    if (e?.imagePath) return `${base}/assets/${this._trimSlash(e.imagePath)}`;

    // 3) nëse vjen snake_case
    if (e?.image_path) return `${base}/assets/${this._trimSlash(e.image_path)}`;

    // 4) fallback
    return `${base}/assets/app_files/Events/default-event.jpg`;
  },

  _trimSlash(p) {
    // heq / në fillim nëse ekziston
    return String(p || "").replace(/^\/+/, "");
  },

  onImgError(e) {
    // vetëm për debug (shiko Console)
    console.log("IMAGE FAILED FOR EVENT:", e?.id, {
      imgClientPath: e?.imgClientPath,
      imageClientPath: e?.imageClientPath,
      imagePath: e?.imagePath,
      image_path: e?.image_path,
      finalUrl: this.getEventImage(e),
    });
  },
}
};
</script>
