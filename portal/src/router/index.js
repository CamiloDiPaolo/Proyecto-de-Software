import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import StatsView from "../views/StatsView.vue";
import DisciplineView from "../views/DisciplineView.vue";
import PaymentView from "../views/PaymentsView.vue";
import MeView from "../views/MeView.vue";

import auth from "./middleware/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/stats",
      name: "estadisticas",
      component: StatsView,
    },
    {
      path: "/discipline/:id",
      name: "disciplina",
      component: DisciplineView,
    },
    {
      path: "/payments",
      name: "pagos",
      component: PaymentView,
    },
    {
      path: "/me",
      name: "miCuenta",
      component: MeView,
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  if (to.name == "login") return next();

  const res = await auth();
  if (res.status == 401) return next({ name: "login" });
  next();
});

export default router;
