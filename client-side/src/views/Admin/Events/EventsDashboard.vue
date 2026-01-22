<template>
	<div class="table-wrapper p-2 events">
		<v-row>
			<v-col cols="9">
				<h2>Events</h2>
			</v-col>
			<v-col cols="3">
				<v-select
					solo
					v-model="selectedCinema"
					:items="getObjectOptionsName(cinemas)"
					@change="changeCinema()"
					label="Select Cinema"
				></v-select>
			</v-col>
		</v-row>

		<hr />
		<div class="d-flex mb-5 events-header">
			<div>
				<v-btn color="success" class="mr-2" @click="onCreateEvent()">
					<v-icon left dark> mdi-plus </v-icon>
					Create Event
				</v-btn>
			</div>
			<div>
				<v-btn
					color="primary"
					:disabled="!isSelected"
					class="mr-2 d-lg-inline action-event-button"
					@click="onEditClick(selected[0].id)"
				>
					Edit
				</v-btn>
				<v-btn
					color="error"
					:loading="removingEvent"
					:disabled="!isSelected || removingEvent"
					class="mr-2 d-lg-inline action-event-button"
					@click="onDeleteClick(selected[0].id)"
				>
					Delete
					<template v-slot:loader>
						<span class="custom-loader">
							<v-icon light>mdi-cached</v-icon>
						</span>
					</template>
				</v-btn>
			</div>
			<v-btn
				:loading="loading"
				:disabled="loading"
				color="blue-grey"
				class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
				@click="onRefresh()"
			>
				Refresh
				<v-icon right dark> mdi-refresh </v-icon>
				<template v-slot:loader>
					<span class="custom-loader">
						<v-icon light>mdi-cached</v-icon>
					</span>
				</template>
			</v-btn>
		</div>
		<!-- DESKTOP -->
		<div class="default-table position-relative d-lg-block">
			<v-data-table
				v-model="selected"
				:single-select="true"
				show-select
				:headers="headers"
				:items="events"
				item-key="id"
				:items-per-page="10"
				:loading="loading"
				loading-text="Loading events... Please wait"
				:class="{ loaded: !loading }"
				class="elevation-1"
			>
				<template v-slot:[`item.name`]="{ item }">
					<a class="link" @click="onDetailsClick(item.id)">{{ item.name }}</a>
				</template>
				<template slot="no-data">
					<div v-if="loading" class="loading-table text-center py-1">
						<b-spinner variant="primary" />
					</div>
					<template v-else>
						<no-data
							no-data-text="No events have been added to this cinema yet..."
							create-text="+ Create event"
							access-page="events"
							@action="onCreateEvent()"
						/>
					</template>
				</template>
			</v-data-table>
		</div>
	</div>
</template>

<script>
export default {
	name: "eventDashboard",
	components: {},
	data() {
		return {
			selected: [],
			headers: [
				{
					text: "Id",
					align: "start",
					sortable: false,
					value: "id",
				},
				{ text: "Title", value: "name" },
				{ text: "Description", value: "description" },
				{ text: "Date", value: "date" },
				{ text: "Price", value: "price" },
				{ text: "Is Paid?", value: "isPaid" },
				{ text: "Attendees", value: "attendeesNumber" },
			],
			selectedCinema: null,
			fields: [
				{
					key: "selected",
					label: "",
					variant: "select",
					hide: true,
				},
				{ key: "id" },
				{ key: "name" },
				{ key: "description" },
				{ key: "date" },
				{ key: "price" },
				{ key: "isPaid" },
				{ key: "attendeesNumber" },
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
		this.getCinemas();
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
					if (this.selectedCinema == null) {
						this.selectedCinema = this.cinemas[0];
					}
					this.getEvents(this.selectedCinema);
				})
				.catch((error) => {
					this.errorToast(
						error.response?.data?.errors[0] ||
							"Something went wrong while fetching events!"
					);
				});
		},
		getEvents(selectedCinema) {
			this.$store.dispatch("getEvents", selectedCinema.id).catch((error) => {
				this.errorToast(
					error.response?.data?.errors[0] ||
						"Something went wrong while fetching movies!"
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
				name: "event-edit",
				params: { cinemaId: this.selectedCinema.id, eventId: eventId },
			});
		},
		onDetailsClick(eventId) {
			this.$router.push({
				name: "event-details",
				params: { cinemaId: this.selectedCinema.id, eventId: eventId },
			});
		},
		onCreateEvent() {
			this.$router.push({
				name: "event-create",
				params: { cinemaId: this.selectedCinema.id },
			});
		},
		onDeleteClick(eventId) {
			this.confirmDelete(
				"Delete Event",
				"Are you sure you want to delete this event?"
			).then((ok) => {
				if (ok) {
					this.$store
						.dispatch("removeEvent", {
							cinemaId: this.selectedCinema.id,
							eventId: eventId,
						})
						.then(() => {
							this.successToast("Event was removed");
							this.selected = [];
							this.getEvents(this.selectedCinema);
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

<style lang="scss" scoped></style>
