import Vue from "vue";
import VueRouter from "vue-router";
import StatusList from "../components/StatusList.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "StatusList",
    component: StatusList,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
