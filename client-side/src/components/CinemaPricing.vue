<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Price for</th>
          <th class="text-left">Euro</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in pricing" :key="item.name">
          <td>{{ item.name }}</td>
          <td>{{ item.price }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  data() {
    return {
      pricing: [
        {
          name: "Cmimi baze i biletes",
          price: "2,50 €",
        },
        {
          name: "Bileta 3D",
          price: "+ 1.00 €",
        },
        {
          name: "Bileta VIP",
          price: "+ 2.00 €",
        },
        {
          name: "Bileta per cifte",
          price: "*2",
        },
      ],
    };
  },
};
</script>
