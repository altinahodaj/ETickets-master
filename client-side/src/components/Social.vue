<template>
	<v-container id="social" tag="section">
		<v-row>
			<v-col cols="12" md="4">
				<instagram />
			</v-col>

			<v-col cols="8" md="8">
				<subscribe />
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: "HomeSocial",

	components: {
		Subscribe: () => import("@/components/Subscribe.vue"),
		Instagram: () => import("@/components/Instagram"),
	},
};
</script>
