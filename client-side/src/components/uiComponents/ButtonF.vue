<template>
  <button>{{ buttonText }}</button>
</template>

<script>
export default {
  name: "ButtonF",
  props: {
    buttonText: {
      type: String,
      default: () => "Label",
    },
  },
};
</script>

<style scoped>
button {
  position: relative;
  padding: 1em 1.8em;
  outline: none;
  border: 1px solid #303030;
  background: #212121;
  color: rgb(25, 118, 210);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 15px;
  overflow: hidden;
  transition: 0.2s;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  margin: 5%;
}
button:hover {
  box-shadow: 0 0 10px rgb(25, 118, 210), 0 0 25px #010102,
    0 0 50px rgb(25, 118, 210);
  transition-delay: 0.6s;
}
button span {
  position: absolute;
}
button span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgb(25, 118, 210));
}
button:hover span:nth-child(1) {
  left: 100%;
  transition: 0.7s;
}
button span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #010102);
}
button:hover span:nth-child(3) {
  right: 100%;
  transition: 0.7s;
  transition-delay: 0.35s;
}
button span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, rgb(25, 118, 210));
}
button:hover span:nth-child(2) {
  top: 100%;
  transition: 0.7s;
  transition-delay: 0.17s;
}
button span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #010102);
}
button:hover span:nth-child(4) {
  bottom: 100%;
  transition: 0.7s;
  transition-delay: 0.52s;
}
button:active {
  background: rgb(25, 118, 210);
  background: linear-gradient(to top right, rgb(25, 118, 210), #010102);
  color: #bfbfbf;
  box-shadow: 0 0 8px rgb(25, 118, 210), 0 0 8px #010102,
    0 0 8px rgb(25, 118, 210);
  transition: 0.1s;
}
button:active
  span:nth-child(1)
  span:nth-child(2)
  span:nth-child(2)
  span:nth-child(2) {
  transition: none;
  transition-delay: none;
}
</style>
