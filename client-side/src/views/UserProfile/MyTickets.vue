<template>
  <div>
    <v-parallax
      dark
      height="400"
      src="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="font-weight-black mb-4">My Tickets</h1>
        </v-col>
      </v-row>
    </v-parallax>
    <div>
      <h1 class="d-flex justify-content-center">My tickets</h1>
      <div v-if="!currentUser || !currentUser.id" class="d-flex justify-content-center">
        <h3>Please login to see your tickets</h3>
      </div>
      <div class="d-flex flex-wrap" v-if="displayTickets.length > 0">
        <div
          class="d-flex flex-wrap mb-15"
          v-for="ticket in displayTickets"
          :key="ticket.id"
        >
          <div class="container ml-2 mr-2">
            <ticket-card-v2 :ticket="ticket" />
          </div>
        </div>
      </div>
      <div v-else-if="currentUser && currentUser.id">
        <h3>You havent bought any tickets</h3>
      </div>
    </div>
  </div>
</template>

<script>
import TicketCardV2 from "@/components/cards/TicketCard-v2.vue";

export default {
  components: { TicketCardV2 },
  data() {
    return {
      fetched: false,
    };
  },
  watch: {
    currentUser: {
      immediate: true,
      handler(u) {
        if (this.fetched) return;
        if (u && u.id) {
          this.getUserTickets();
          this.fetched = true;
        }
      },
    },
  },
  computed: {
    loading() {
      return this.$store.state.tickets.loading;
    },
    userTickets() {
      return this.$store.state.tickets.userTickets;
    },
    displayTickets() {
      const list = this.userTickets || [];
      if (!list.length) return [];

      // Backend returns tickets sorted by createdAt desc.
      // We treat createdAt as "reservation time" so tickets with the same timestamp
      // belong to the same (latest) purchase.
      const latestTs = String(list[0]?.createdAt || list[0]?.created_at || "");
      if (!latestTs) return list;

      return list.filter(
        (t) => String(t?.createdAt || t?.created_at || "") === latestTs
      );
    },
    currentUser() {
      return this.$store.state.users.user;
    },
  },
  methods: {
    getUserTickets() {
      if (!this.currentUser || !this.currentUser.id) return;
      const query = {
        userId: this.currentUser.id,
      };
      this.$store.dispatch("getUserTickets", query).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching tickets!"
        );
      });
    },
  },
};
</script>
<style lang="css"></style>
