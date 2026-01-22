<template>
  <div>
    <div v-if="loading"><loading-page /></div>
    <div v-else>
      <v-sheet class="mx-auto" elevation="8">
        <v-sheet
          class="d-flex justify-content-center mx-auto"
          elevation="10"
          max-height="1000"
        >
          <div v-if="!actors.length > 0">
            <h5>There are no actors for this movie.</h5>
          </div>
          <v-container v-else>
            <v-slide-group
              class="d-flex justify-content-center ma-2"
              active-class="success"
              multiple
              show-arrows="always"
            >
              <v-slide-item
                v-for="actor in actors"
                :key="actor.id"
                class="mb-2 d-flex justify-content-center"
              >
                <div class="pa-4 ml-4 mr-4">
                  <v-row justify="center">
                    <v-card class="p-2 mx-auto" max-width="250" outlined>
                      <div class="d-flex">
                        <v-list-item-content>
                          <div class="text-overline mb-4">
                            <v-img
                              height="200"
                              width="200"
                              :src="actor.photos[0].imgClientPath"
                              class="avatar-image"
                            ></v-img>
                          </div>

                          <v-list-item-title class="text-h6 mb-1">
                            {{ actor.firstName }} {{ actor.lastName }}
                          </v-list-item-title>
                        </v-list-item-content>
                      </div>
                    </v-card>
                  </v-row>
                </div>
              </v-slide-item>
            </v-slide-group>
          </v-container>
        </v-sheet>
      </v-sheet>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  created() {},
  watch: {
    movie() {
      return this.getMovieActors();
    },
  },
  computed: {
    loading() {
      return this.$store.state.movieTimes.loading;
    },
    movie() {
      return this.$store.state.movies.movie;
    },
    actors() {
      return this.$store.state.movies.movie.actors;
    },
  },
  methods: {},
};
</script>
