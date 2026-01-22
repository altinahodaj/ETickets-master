<template>
<validation-observer ref="observer" v-slot="{ invalid }">
<v-form ref="form" v-model="valid" lazy-validation @submit.prevent="createReview">
<!-- Title -->
<validation-provider v-slot="{ errors }" name="Title" rules="required|min:5">
<v-text-field
v-model="reviewTitle"
name="reviewTitle"
:counter="30"
:error-messages="errors"
:rules="nameRules"
label="Review Title"
required
/>
</validation-provider>

<!-- Description -->
<validation-provider v-slot="{ errors }" name="Description" rules="required">
<v-text-field
v-model="reviewDescription"
name="reviewDescription"
:rules="descRules"
:error-messages="errors"
:counter="300"
label="Review Description"
required
/>
</validation-provider>

<!-- Rating -->
<validation-provider v-slot="{ errors }" name="Rating" rules="required|min_value:1">
<label for="v-rating">Rating</label>
<v-rating
id="v-rating"
v-model="reviewRating"
style="margin-top: 10px; margin-bottom: 30px"
color="amber"
dense
required
/>
<div
v-if="errors && errors.length"
style="color: #b00020; font-size: 12px; margin-top: 6px;"
>
{{ errors[0] }}
</div>
</validation-provider>

<v-btn
type="button"
color="success"
class="mr-4"
:disabled="invalid || loading"
@click="createReview"
>
Post Review
</v-btn>

<v-btn type="button" color="error" class="mr-4" @click="resetForm">
Reset Form
</v-btn>

<div v-if="errorMsg" style="margin-top: 12px; color: #b00020;">
{{ errorMsg }}
</div>
</v-form>
</validation-observer>
</template>

<script>
import { ValidationObserver, ValidationProvider, setInteractionMode } from "vee-validate";

setInteractionMode("eager");

export default {
name: "AddReview",
components: { ValidationProvider, ValidationObserver },

data: () => ({
valid: true,
movieId: null,

nameRules: [
(v) => !!v || "Title is required",
(v) => (v && v.length <= 30) || "Title must be less than 30 characters",
],
descRules: [
(v) => !!v || "Description is required",
(v) => (v && v.length <= 300) || "Description must be less than 300 characters",
],

reviewTitle: "",
reviewDescription: "",
reviewRating: 0,

loading: false,
errorMsg: null,
}),

computed: {
user() {
return this.$store.state.users.user; // ✅ do vijë nga Firebase (main.js)
},
loggedIn() {
return this.$store.state.users.loggedIn;
},
},

created() {
this.movieId = Number(this.$route.params.movieId);
},

methods: {
resetForm() {
if (this.$refs.form) this.$refs.form.reset();
this.clear();
},

async createReview() {
this.errorMsg = null;

// ✅ mos lejo post nese s’je logged-in
if (!this.loggedIn || !this.user || !this.user.id) {
this.errorMsg = "Duhet me qenë logged in për me postu review.";
return;
}

if (this.loading) return;
this.loading = true;

try {
const review = {
review_title: this.reviewTitle,
review_description: this.reviewDescription,
review_rating: this.reviewRating,
user_id: this.user.id,
user_name: this.user.displayName || this.user.email || "User",
};

await this.$store.dispatch("createReview", { movieId: this.movieId, review });

this.clear();
this.$router.push({ name: "Movies" });
} catch (error) {
console.log(error);
this.errorMsg = "Nuk u postua review. Shiko console/network për detaje.";
} finally {
this.loading = false;
}
},

clear() {
this.reviewTitle = "";
this.reviewDescription = "";
this.reviewRating = 0;
if (this.$refs.observer) this.$refs.observer.reset();
},
},
};
</script>

<style scoped>
/* opsionale */
</style>