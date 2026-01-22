<template>
	<div>
		<section id="welcome" class="overflow-hidden">
			<v-row no-gutters>
				<v-col class="hidden-sm-and-down" md="6">
					<v-img :src="photo1" height="50vh" width="50vw" />
				</v-col>

				<v-col
					class="align-content-space-between layout wrap"
					cols="12"
					md="6"
					:pa-5="$vuetify.breakpoint.smAndDown"
				>
					<!-- <base-bubble-1 style="transform: rotate(180deg) translateY(25%)" /> -->

					<v-row align="center" justify="center">
						<v-col cols="10" md="6">
							<h1 class="test">About Us!</h1>
							<p class="test">
								CinemaVerse, as the first project in our region for the union of
								cinemas, is a big project that is doing very well because it is
								easy to use and you have everything in one place. CinemaVerse
								was created with the aim of bringing customers together in one
								platform, through comments, movie selection and online payment.
							</p>
							<!-- <base-btn class="mt-4"> Learn More! </base-btn> -->
						</v-col>
					</v-row>

					<!-- <base-bubble-2
						style="transform: rotate(180deg) translate(-200px, -15%)"
					/> -->
				</v-col>
			</v-row>
		</section>
		<section id="welcome" class="overflow-hidden">
			<v-row no-gutters>
				<v-col
					class="align-content-space-between layout wrap"
					cols="12"
					md="6"
					:pa-5="$vuetify.breakpoint.smAndDown"
				>
					<!-- <base-bubble-1 style="transform: rotate(180deg) translateY(25%)" /> -->

					<v-row align="center" justify="center">
						<v-col cols="10" md="6">
							<h1>Mission!</h1>
							<p>
								As an application that is at the beginning, we are trying to be
								the best in the work we do, where we still continue to work
								towards the quality and maintenance of the application. Our
								mission for the future is to spread even more through the
								neighboring countries, to have as many cinemas from different
								countries as possible and in this way to expand even more.
							</p>
							<!-- <base-btn class="mt-4"> Learn More! </base-btn> -->
						</v-col>
					</v-row>

					<!-- <base-bubble-2
						style="transform: rotate(180deg) translate(-200px, -15%)"
					/> -->
				</v-col>
				<v-col class="hidden-sm-and-down" md="6">
					<v-img :src="photo2" height="50vh" width="50vw" />
				</v-col>
			</v-row>
		</section>
		<section id="welcome" class="overflow-hidden">
			<v-row no-gutters>
				<v-col class="hidden-sm-and-down" md="6">
					<v-img :src="photo3" height="50vh" width="50vw" />
				</v-col>

				<v-col
					class="align-content-space-between layout wrap"
					cols="12"
					md="6"
					:pa-5="$vuetify.breakpoint.smAndDown"
				>
					<!-- <base-bubble-1 style="transform: rotate(180deg) translateY(25%)" /> -->

					<v-row align="center" justify="center">
						<v-col cols="10" md="6">
							<h1>Experience!</h1>
							<p>
								Considering that CinemaVerse is the first application in our
								market, it has been well received by our clients, where we have
								also received feedback, very good comments. So we are working
								for the best
							</p>
							<!-- <base-btn class="mt-4"> Learn More! </base-btn> -->
						</v-col>
					</v-row>

					<!-- <base-bubble-2
						style="transform: rotate(180deg) translate(-200px, -15%)"
					/> -->
				</v-col>
			</v-row>
		</section>
	</div>
</template>

<script>
export default {
	data() {
		return {
			photo1:
				"https://www.cineplexx-ks.eu/GenticsImageStore/952/353/force//media/mobile/ks/center/5.jpg",
			photo2:
				"https://qkk-rks.com/uploads/images/2018/March/12/auto_cineplexx1520872988.jpg",
			photo3:
				"https://qkk-rks.com/uploads/images/2018/March/12/auto_kinoabc11520873925.jpg",
		};
	},
};
</script>

<style scoped>
.test {
	margin-top: revert;
}
</style>
