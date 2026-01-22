<template>
	<v-container id="subscribe" tag="section">
		<v-card color="rgba(203, 170, 92, 0.51)" class="pa-3">
			<v-container>
				<v-row>
					<v-col cols="12" md="10" offset-md="1">
						<h1>Contact</h1>

						<v-list class="transparent">
							<v-list-item>
								<v-list-item-avatar color="primary">
									<v-icon class="elevation-4" dark> mdi-email-outline </v-icon>
								</v-list-item-avatar>

								<v-list-item-title>EMAIL</v-list-item-title>

								<v-list-item-subtitle>
									INFO@CINEMAVERSE.COM
								</v-list-item-subtitle>
							</v-list-item>

							<v-list-item>
								<v-list-item-avatar color="primary">
									<v-icon class="elevation-4" dark> mdi-map-marker </v-icon>
								</v-list-item-avatar>

								<v-list-item-title>ADDRESS</v-list-item-title>

								<v-list-item-subtitle> PRISHTINE </v-list-item-subtitle>
							</v-list-item>

							<v-list-item>
								<v-list-item-avatar color="primary">
									<v-icon class="elevation-4" dark> mdi-phone </v-icon>
								</v-list-item-avatar>

								<v-list-item-title>PHONE</v-list-item-title>

								<v-list-item-subtitle> +38344123456 </v-list-item-subtitle>
							</v-list-item>
						</v-list>
					</v-col>
				</v-row>
			</v-container>
		</v-card>
	</v-container>
</template>

<script>
export default {
	name: "HomeSubscribe",
};
</script>
