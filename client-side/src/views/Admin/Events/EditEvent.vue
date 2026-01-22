<template>
	<div>
		<h2>Edit Event</h2>
		<div class="container mt-5">
			<validation-observer ref="observer" v-slot="{ invalid }">
				<form @submit.prevent="submit">
					<validation-provider
						v-slot="{ errors }"
						name="Name"
						rules="required|min:3"
					>
						<v-text-field
							v-model="event.name"
							:error-messages="errors"
							label="Name"
							outlined
							required
						></v-text-field>
					</validation-provider>
					<validation-provider
						v-slot="{ errors }"
						name="Description"
						rules="required"
					>
						<v-textarea
							v-model="event.description"
							:error-messages="errors"
							label="Description"
							outlined
							required
						></v-textarea>
					</validation-provider>
					<validation-provider v-slot="{ errors }" name="date" rules="required">
						<v-text-field
							v-model="event.date"
							type="datetime-local"
							name=""
							:error-messages="errors"
							label="Event Date"
							outlined
							required
						></v-text-field>
					</validation-provider>
					<validation-provider
						v-slot="{ errors }"
						name="price"
						rules="required"
					>
						<v-text-field
							v-model="event.price"
							type="number"
							name=""
							:error-messages="errors"
							label="Price"
							outlined
							required
						></v-text-field>
					</validation-provider>
					<validation-provider
						v-slot="{ errors }"
						name="attendeesNumber"
						rules="required"
					>
						<v-text-field
							v-model="event.attendeesNumber"
							type="number"
							name=""
							:error-messages="errors"
							label="Attendees"
							outlined
							required
						></v-text-field>
					</validation-provider>
					<v-switch v-model="event.isPaid" :label="`Is Paid?`"></v-switch>
					<v-btn
						color="success"
						type="submit"
						:disabled="invalid"
						class="mr-2"
						@click="editEvent()"
					>
						Submit
					</v-btn>
				</form>
			</validation-observer>
		</div>
	</div>
</template>

<script>
import { required, numberInt, minValueRule } from "@/helpers/validations";
import {
	ValidationObserver,
	ValidationProvider,
	setInteractionMode,
} from "vee-validate";

setInteractionMode("eager");

export default {
	components: {
		ValidationProvider,
		ValidationObserver,
	},
	data() {
		return {
			cinemaId: null,
			eventId: null,
			required,
			numberInt,
			minValueRule,
			// name: "",
			// description: "",
			// date: "date",
			// isPaid: "",
			// price:"",
			// attendeesNumber:"",
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
		getEvent(query) {
			this.$store.dispatch("getEvent", query).catch((error) => {
				this.errorToast(
					error.response?.data?.errors[0] ||
						"Something went wrong while fetching event!"
				);
			});
		},
		editEvent() {
			const event = {
				id: this.eventId,
				name: this.event.name,
				description: this.event.description,
				date: this.event.date,
				isPaid: this.event.isPaid,
				price: this.event.price,
				attendeesNumber: this.event.attendeesNumber,
			};
			this.$store
				.dispatch("editEvent", { cinemaId: this.cinemaId, event: event })
				.then(() => {
					this.clear();
					this.$router.push({
						name: "EventsDashboard",
					});
				})
				.catch((error) => {
					this.errorToast(
						error.response?.data?.errors[0] ||
							"Something went wrong while creating events!"
					);
				});
		},

		clear() {
			this.name = "";
			this.description = "";
			this.date = "";
			this.isPaid = "";
			(this.price = ""),
				(this.attendeesNumber = ""),
				this.$refs.observer.reset();
		},
	},
};
</script>

<style></style>
