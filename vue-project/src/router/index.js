import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
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
  ],
});

router.beforeEach(async (to, from, next) => {
  // si no hay una middleware seguimos de largo
  if (to.name == "login") return next();

  const res = await auth();
  if (res.status == 401) return next({ name: "login" });
  next();
}); 

export default router;
