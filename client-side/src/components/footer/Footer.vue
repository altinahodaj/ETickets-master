<template>
	<v-footer dark padless>
		<v-card flat tile class="primary lighten-1 white--text text-center">
			<v-card-text>
				<!-- <v-btn flat v-for="icon in icons" :key="icon" class="mx-4 white--text" icon>
          <v-icon size="24px">
            {{ icon }}
          </v-icon>
        </v-btn>  -->
			</v-card-text>

			<v-card-text class="white--text pt-0">
				Phasellus feugiat arcu sapien, et iaculis ipsum elementum sit amet.
				Mauris cursus commodo interdum. Praesent ut risus eget metus luctus
				accumsan id ultrices nunc. Sed at orci sed massa consectetur dignissim a
				sit amet dui. Duis commodo vitae velit et faucibus. Morbi vehicula
				lacinia malesuada. Nulla placerat augue vel ipsum ultrices, cursus
				iaculis dui sollicitudin. Vestibulum eu ipsum vel diam elementum tempor
				vel ut orci. Orci varius natoque penatibus et magnis dis parturient
				montes, nascetur ridiculus mus.
			</v-card-text>

			<v-divider></v-divider>

			<v-card-text class="white--text">
				{{ new Date().getFullYear() }} — <strong>CinemaVerse</strong>
			</v-card-text>
			<div class="py-4" dark height="auto">
				<v-container class="mx-auto">
					<v-row>
						<v-btn
							class="mr-2"
							color="secondary"
							square
							title="Go to top"
							@click="$vuetify.goTo(0)"
						>
							<v-icon>mdi-chevron-up</v-icon>
						</v-btn>
					</v-row>
				</v-container>
			</div>
		</v-card>
	</v-footer>
</template>

<script>
export default {
	name: "Footer",

	data() {
		return {
			components: {},
		};
	},
};
</script>
<!--<template>
	<v-footer class="py-4" dark height="auto">
		<v-container class="mx-auto d-flex">
			<v-row>
				<v-col cols="9">
					<base-btn
						v-for="(item, i) in items"
						:key="i"
						:href="item.href"
						class="ml-0 mr-3"
						color="primary"
						square
						target="_blank"
					>
						<v-icon v-text="item.icon" />
					</base-btn>
				</v-col>

				<v-card-text class="white--text">
					{{ new Date().getFullYear() }} — <strong>CinemaVerse</strong>
				</v-card-text>

				<v-spacer />

				<base-btn
					class="mr-0"
					square
					title="Go to top"
					@click="$vuetify.goTo(0)"
				>
					<v-icon>mdi-chevron-up</v-icon>
				</base-btn>
			</v-row>
		</v-container>
	</v-footer>
</template>

<script>
export default {
	name: "CoreFooter",

	data: () => ({
		items: [
			{
				href: "#!",
				icon: "mdi-twitter",
			},
			{
				href: "#!",
				icon: "mdi-instagram",
			},
			{
				href: "#!",
				icon: "mdi-facebook",
			},
			{
				href: "#!",
				icon: "mdi-google-plus",
			},
			{
				href: "#!",
				icon: "mdi-reddit",
			},
			{
				href: "#!",
				icon: "mdi-discord",
			},
			{
				href: "#!",
				icon: "mdi-pinterest",
			},
		],
	}),
};
</script>-->
