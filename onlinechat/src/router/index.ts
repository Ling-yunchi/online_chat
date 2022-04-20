import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
  RouteRecordRaw,
} from "vue-router";
import HomeView from "../views/home/HomeView.vue";
import LoginView from "../views/login/LoginView.vue";
import WelcomeView from "../views/WelcomeView.vue";
import RegisterView from "../views/login/RegisterView.vue";
import ChatListView from "../views/home/chat/ChatListView.vue";
import ChatView from "../views/home/chat/ChatView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "welcome",
    component: WelcomeView,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterView,
  },
  {
    path: "/home",
    name: "home",
    component: HomeView,
    children: [
      {
        path: "",
        component: ChatListView,
      },
      {
        path: "chatList",
        name: "ChatList",
        component: ChatListView,
      },
      {
        path: "chat/:roomId",
        name: "Chat",
        component: ChatView,
        props: true,
      },
    ],
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
];

const router = createRouter({
  // TODO: 部署时修改基本路径
  history: createWebHashHistory("/wr_web/online_chat"),
  routes,
});

export default router;
