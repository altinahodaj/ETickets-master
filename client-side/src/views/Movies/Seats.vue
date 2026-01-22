<template>
  <div class="container">
    <div class="screen">
      <p class="font-weight-bold">Screen</p>
    </div>

    <div class="seats">
      <div class="row">
        <div class="col seat"
          v-for="seat in seats"
          :key="seat.id"
          :id="seat.id"
          v-text="seat.id"
          :class="seat.available ? 'available' : 'unavailable'"
          @click="selectSeat"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      seats: [
        { id: 'A1', available: true },
        { id: 'A2', available: true },
        { id: 'A3', available: false },
        { id: 'A4', available: false },
        { id: 'A5', available: true },
        { id: 'A6', available: true },
    ]}
  },

  methods: {
    selectSeat (event) {
      let seat = this.seats.find(seat => seat.id === event.target.id)
      seat.available = !seat.available
    }
  }
}
</script>

<style lang="css" scoped>
  .screen {
    background-color: #2b6282;
  }

  .screen p {
    color: white;
    font-size: 18px;
  }

  .seats {
    margin-top: 50px;
    
  }

  .seat {
    color: white;
    margin: 3px;
    font-weight: bold;
    cursor: pointer;
  }

  .available {
    background-color: #2d4d86;
  }

  .unavailable {
    background-color: #73264f;
  }
</style>
