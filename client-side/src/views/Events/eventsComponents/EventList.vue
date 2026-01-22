<template>
  <div class="card mt-4">
    <table class="table m-0">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Name</th>
          <th scope="col">Description</th>
          <th scope="col">Date</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="{ id, name, description,date } in events"
          :key="id"
        >
          <td>{{ id }}</td>
          <td>{{ name }}</td>
          <td>{{ description }}</td>
          <td>{{ date }}</td>
          <td>
            <router-link :to="`/edit/${id}`">
              <button class="btn btn-primary btn-sm me-2">Edit</button>
            </router-link>
            <button class="btn btn-danger btn-sm" @click="deleteEvent(id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "eventList",
   data() {
    return {
      selected: [],
      selectedCinema: null,
      fields: [
        {
          key: "selected",
          label: "",
          variant: "select",
          hide: true,
        },
        { key: "id" },
        { key: "Name" },
        { key: "Description" },
        { key: "Date" },
      ],
    };
  },
  computed: {
    loading() {
      return this.$store.state.events.loading;
    },
    events() {
      return this.$store.state.events.events;
    },
    cinemas() {
      return this.$store.state.cinemas.cinemas;
    },
    removingEvent() {
      return this.$store.state.events.removingEvent;
    },
    isSelected() {
      return this.selected[0];
    },
  },
  created() {
    this.getEvents();
  },
  methods: {
    onRowSelected(item) {
      this.selected = item;
    },
    onRefresh() {
      this.getEvents(this.selectedEvent);
    },
    getCinemas() {
      this.$store
        .dispatch("getCinemas")
        .then(() => {
          if (this.selectedEvent == null) {
            this.selectedEvent = this.events[0];
          }
          this.getEvents(this.selectedEvent);
        })
        .catch((error) => {
          this.errorToast(
            error.response?.data?.errors[0] ||
              "Something went wrong while fetching cinemas!"
          );
        });
    },
    getEvents(selectedCinema) {
      this.$store.dispatch("getEvents", selectedCinema.id).catch((error) => {
        this.errorToast(
          error.response?.data?.errors[0] ||
            "Something went wrong while fetching events!"
        );
      });
    },
    changeCinema() {
      if (this.selectedCinema != null) {
        this.getEvents(this.selectedCinema);
      }
    },
    onEditClick(eventId) {
      this.$router.push({
        name: "movie-edit",
        params: { eventId },
      });
    },
    onDetailsClick(eventId) {
      this.$router.push({
        name: "movie-details",
        params: { eventId },
      });
    },
    onCreateEvent() {
      this.$router.push({
        name: "event-create",
      });
    },
    onDeleteClick(eventId) {
      this.confirmDelete(
        "Delete Event",
        "Are you sure you want to delete this event?"
      ).then((ok) => {
        if (ok) {
          this.$store
            .dispatch("events/removeEvent", eventId)
            .then(() => {
              this.successToast("Event was removed");
              this.selected = [];
              this.getEvents(this.selectedCinema.id);
            })
            .catch((error) => {
              this.errorToast(error.response.data.errors[0]);
            });
        }
      });
    },
  },
};
</script>
