<template>
  <div class="movie-actors-container">
    <div v-if="loading" class="d-flex justify-center pa-10">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    <div v-else>
      <div v-if="!actors || !actors.length" class="no-actors pa-10 text-center">
        <v-icon size="64" color="grey lighten-1">mdi-account-off-outline</v-icon>
        <h5 class="grey--text text--darken-1 mt-4">There are no actors listed for this movie yet.</h5>
      </div>
      
      <v-slide-group
        v-else
        show-arrows="always"
        class="py-4"
      >
        <v-slide-item
          v-for="actor in actors"
          :key="actor.id"
        >
          <v-card
            class="actor-card ma-4"
            elevation="2"
            @click="onActorClick(actor.id)"
          >
            <v-img
              v-if="actor.photos && actor.photos.length"
              :src="actor.photos[0].imgClientPath"
              height="240"
              cover
              class="actor-image"
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                </v-row>
              </template>
            </v-img>
            <v-img
              v-else
              src="/assets/app_files/Actors/default-actor.jpg"
              height="240"
              cover
              class="actor-image grey lighten-3"
            ></v-img>
            
            <v-card-text class="text-center pa-3">
              <div class="actor-name">{{ actor.firstName }} {{ actor.lastName }}</div>
              <div class="actor-role grey--text text-caption">Actor</div>
            </v-card-text>
          </v-card>
        </v-slide-item>
      </v-slide-group>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {
    loading() {
      return this.$store.state.movies.loading;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
    actors() {
      return this.$store.state.movies.movie?.actors || [];
    },
  },
  methods: {
    onActorClick(actorId) {
      this.$router.push({
        name: "actor-details",
        params: { id: actorId },
      });
    },
  },
};
</script>

<style scoped>
.movie-actors-container {
  width: 100%;
}

.actor-card {
  width: 180px;
  border-radius: 12px !important;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.actor-card:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.actor-image {
  border-bottom: 3px solid #1867c0;
}

.actor-name {
  font-weight: 700;
  font-size: 15px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-actors {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 150px;
}
</style>
