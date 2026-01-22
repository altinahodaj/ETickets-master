<template>
	<div>
		<div>
			<v-carousel v-model="model">
				<v-carousel-item v-for="(color, i) in colors" :key="color">
					<v-sheet :color="color" height="100%" tile>
						<v-row class="fill-height" align="center" justify="center">
							<div class="text-h2">Fotot e cinemave {{ i + 1 }}</div>
						</v-row>
					</v-sheet>
				</v-carousel-item>
			</v-carousel>
		</div>
		<div>
			<div class="d-inline pa-2">
				<h1>ABC</h1>
				<p>Te Sheshi Nena Tereze, 10000 Prishtina</p>
			</div>
			<div class="view">
				<router-link :to="{ name: 'Cineplexx' }">
					Movies / Tickets
				</router-link>
			</div>
		</div>
		<div>
			<h1>Map ( Nese mujna me implementu)</h1>
			<img src="@/assets/joker.jpg" class="foto" alt="" />
		</div>
		<!-- <div>
			<div class="d-inline pa-2 deep-purple accent-4 white--text">
				Cineplexx Prishtine / Prizren
			</div>
			<div class="d-inline pa-2 black white--text">
				<router-link :to="{ name: 'Cineplexx' }"> View Movies </router-link>
			</div>
		</div> -->
	</div>
</template>

<script>
export default {
	data: () => ({
		drawer: null,
		model: 0,
		colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
	}),
};
</script>

<style scoped>
.view {
	display: flex;
	justify-content: end;
}
.foto {
	height: 20%;
	width: 100%;
}
</style>
