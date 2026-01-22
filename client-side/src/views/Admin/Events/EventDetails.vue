<template>
	<div>
		<div v-if="loading"><loading-page /></div>
		<div v-else>
			<v-row>
				<v-col cols="9">
					<h2>Event Details</h2>
				</v-col>
				<v-col class="d-flex align-content-end" cols="3">
					<v-btn
						class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
						color="success"
						@click="redirectToAddPhoto(cinemaId, eventId)"
					>
						<v-icon left dark> mdi-camera </v-icon>
						Add Images
					</v-btn>
					<v-btn
						class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
						color="primary"
						@click="redirectToEventTimes(cinemaId, eventId)"
					>
						<v-icon left dark> schedule </v-icon>
						View Schedule
					</v-btn>
				</v-col>
			</v-row>

			<hr />
			<div class="container mt-5">
				<v-col class="d-flex align-center justify-content-center" cols="12">
					<v-item v-if="event.photos.length > 0">
						<v-carousel>
							<v-carousel-item
								v-for="(photo, i) in event.photos"
								:key="i"
								:src="photo.imgClientPath"
								reverse-transition="fade-transition"
								transition="fade-transition"
							>
								<div class="d-flex align-content-end p-3">
									<v-btn
										class="mt-1 mt-sm-0 ml-auto mr-0 white--text"
										color="error"
										@click="removePhoto(cinemaId, eventId, photo)"
									>
										<v-icon left dark> mdi-close </v-icon>
										Remove
									</v-btn>
								</div>
							</v-carousel-item>
						</v-carousel>
					</v-item>
					<div v-else class="d-flex flex-column mb-5">
						<h2>There are no photos for this event!</h2>
						<v-btn
							color="success"
							class="mr-2"
							@click="redirectToAddPhoto(cinemaId, eventId)"
						>
							<v-icon left dark> mdi-camera </v-icon>
							Add Image
						</v-btn>
					</div>
				</v-col>

				<v-item-group active-class="primary">
					<v-container>
						<v-row>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Title:
										<h6>{{ event.name }}</h6>
									</span>
								</v-item>
							</v-col>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Description:
										<h6>{{ event.description }}</h6></span
									>
								</v-item>
							</v-col>

							<v-col cols="12" md="4">
								<v-item>
									<span
										>Is it paid:
										<h6>{{ event.isPaid }}</h6></span
									>
								</v-item>
							</v-col>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Price:
										<h6>{{ event.price }}</h6></span
									>
								</v-item>
							</v-col>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Date:
										<h6>{{ event.date }}</h6></span
									>
								</v-item>
							</v-col>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Attendees Number:
										<h6>{{ event.attendeesNumber }}</h6></span
									>
								</v-item>
							</v-col>
							<!-- <v-col cols="12" md="4">
								<v-item>
									<span
										>Language:
										<h6>{{ event.language }}</h6></span
									>
								</v-item>
							</v-col>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Genre:
										<h6>{{ event.genre }}</h6></span
									>
								</v-item>
							</v-col>
							<v-col cols="12" md="4">
								<v-item>
									<span
										>Movie Length (minutes):
										<h6>{{ event.length }}</h6></span
									>
								</v-item>
							</v-col> -->
						</v-row>
					</v-container>
				</v-item-group>
				<div></div>
			</div>
		</div>
	</div>
</template>

<script>
import { required, numberInt, minValueRule } from "@/helpers/validations";
import { setInteractionMode } from "vee-validate";

setInteractionMode("eager");

export default {
	components: {},
	data() {
		return {
			cinemaId: null,
			eventId: null,
			required,
			numberInt,
			minValueRule,
		};
	},
	created() {
		this.cinemaId = this.$route.params.cinemaId;
		this.eventId = this.$route.params.eventId;
		const query = {
			cinemaId: this.cinemaId,
			eventId: this.eventId,
		};
		this.getEvent(query);
	},
	computed: {
		loading() {
			return this.$store.state.events.loading;
		},
		event() {
			return this.$store.state.events.event;
		},
	},
	methods: {
		submit() {
			this.$refs.observer.validate();
		},
		removePhoto(cinemaId, eventId, photo) {
			this.$store
				.dispatch("removeEventPhoto", {
					cinemaId: cinemaId,
					eventId: eventId,
					photoId: photo.longId,
				})
				.then(() => {
					this.getEvent({ cinemaId: cinemaId, eventId: eventId });
				})
				.catch((error) => {
					this.errorToast(
						error.response?.data?.errors[0] ||
							"Something went wrong while deleting photo!"
					);
				});
		},
		getEvent(query) {
			this.$store.dispatch("getEvent", query).catch((error) => {
				this.errorToast(
					error.response?.data?.errors[0] ||
						"Something went wrong while fetching movie!"
				);
			});
		},
		redirectToAddPhoto(cinemaId, eventId) {
			this.$router.push({
				name: "event-add-photo",
				params: { cinemaId: cinemaId, eventId: eventId },
			});
		},
		redirectToEventTimes(cinemaId, eventId) {
			this.$router.push({
				name: "event-times",
				params: { cinemaId: cinemaId, eventId: eventId },
			});
		},
	},
};
</script>
