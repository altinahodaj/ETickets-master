// const { defineConfig } = require("@vue/cli-service");
const path = require("path");

module.exports = {
  publicPath:
    process.env.NODE_ENV === "production" ? "/production-sub-path/" : "/",

  configureWebpack: {
    resolve: {
      alias: {
        "@core": path.resolve(__dirname, "src/@core"),
        "@validations": path.resolve(__dirname, "src/helpers/validations.js"),
        "@axios": path.resolve(__dirname, "src/libs/axios"),
      },
    },
  },
  transpileDependencies: ["vuetify"],
};
