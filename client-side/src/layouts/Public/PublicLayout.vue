<template>
	<v-app>
		<navigation :isLoggedIn="isLoggedIn" :auth="auth" />
		<v-main class="ma-4">
			<router-view />
		</v-main>
		<app-footer />
	</v-app>
</template>

<script>
import Navigation from "@/components/navbar/Navigation.vue";
import AppFooter from "@/components/footer/Footer.vue";

export default {
	name: "PublicLayout",
	components: { Navigation, AppFooter },

	props: {
		isLoggedIn: {
			required: true,
			type: Boolean,
		},
		auth: {
			required: true,
		},
	},

	data() {
		return {};
	},
	computed: {},
};
</script>
