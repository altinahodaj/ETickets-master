import Vue from "vue";
import ButtonLoading from "@/components/buttons/ButtonLoading.vue";
import LoadingPage from "@/components/LoadingPage.vue";
import TableBusy from "@/components/table/TableBusy.vue";
import TableNoData from "@/components/table/TableNoData.vue";
import PaperSimple from "@/components/paper/PaperSimple.vue";
import SelectButton from "@/@core/components/select-button/SelectButton.vue";
import CustomSelect from "@/components/form/CustomSelect.vue";

Vue.component("button-loading", ButtonLoading);
Vue.component("loading-page", LoadingPage);
Vue.component("table-busy", TableBusy);
Vue.component("no-data", TableNoData);
Vue.component("paper-simple", PaperSimple);
Vue.component("select-button", SelectButton);
Vue.component("custom-select", CustomSelect);
