import { format } from "date-fns";

const helpers = {
  methods: {
    movieScheduleDateTime: (isoDate) =>
      isoDate ? format(new Date(`${isoDate}Z`), "dd MMMM - HH:mm") : "-",
    formatSimpleDateTime: (isoDate) =>
      isoDate ? format(new Date(`${isoDate}Z`), "yyyy-MM-dd") : "-",
    formatShortDateTime: (isoDate) =>
      isoDate ? format(new Date(`${isoDate}Z`), "yyyy-MM-dd HH:mm") : "-",
    formatDateTime: (isoDate) =>
      isoDate ? format(new Date(`${isoDate}`), "yyyy-MM-dd HH:mm:ss") : "-",

    getOptions: (options) =>
      options.map((o) => ({ text: o.value, value: o.id })),
    getObjectOptions: (options) => {
      const keys = Object.keys(options);
      return keys.map((key) => ({ text: key, value: options[key] }));
    },
    getObjectOptionsName: (options) => {
      const keys = Object.keys(options);
      return keys.map((key) => ({
        text: options[key].name,
        value: options[key],
      }));
    },
    getActorNames: (options) => {
      const keys = Object.keys(options);
      return keys.map((key) => ({
        text: `${options[key].firstName} ${options[key].lastName}`,
        value: options[key],
      }));
    },
    getObjectText: (options, id) => options.find((o) => o.value === id)?.text,
    getObjectName: (options, id) => options.find((o) => o.value === id)?.name,
    getObjectOptionsText: (options, id) => {
      const keys = Object.keys(options);
      const opt = keys.map((key) => ({ text: key, value: options[key] }));
      return opt.find((o) => o.value === id)?.text;
    },
    errorToast(message, title = "Error") {
      this.generalToast(message, title, "danger");
    },
    successToast(message, title = "Success") {
      this.generalToast(message, title, "success");
    },
    infoToast(message, title = "Info") {
      this.generalToast(message, title, "primary");
    },
    generalToast(message, title, variant) {
      this.$bvToast.toast(message, {
        toastClass: "general-toast-class",
        solid: true,
        autoHideDelay: 2000,
        title,
        variant,
      });
    },
    confirmDelete(
      title = "Delete",
      message = "Are you sure you want to delete?",
      okTitle = "Delete",
      cancelTitle = "Cancel"
    ) {
      return this.$bvModal
        .msgBoxConfirm(message, {
          title,
          okVariant: "danger",
          okTitle,
          cancelTitle,
          cancelVariant: "bg-white",
          hideHeaderClose: false,
          centered: true,
        })
        .catch();
    },
  },
};

export default helpers;
