<template>
	<v-container class="pa-0">
		<!-- <base-subheading>On Instagram</base-subheading> -->

		<v-row>
			<v-col v-for="(post, i) in posts" :key="i" cols="4">
				<v-card :href="post.href" color="grey lighten-2" height="88" tag="a">
					<v-img
						v-if="post.src"
						:src="require(`@/assets/instagram/${post.src}`)"
						height="100%"
					/>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: "Instagram",

	data: () => ({
		posts: [
			{ src: "1.jpg" },
			{ src: "2.jpg" },
			{ src: "3.jpg" },
			{ src: "4.jpg" },
			{ src: "5.jpg" },
			{ src: "6.jpg" },
		],
	}),
};
</script>
