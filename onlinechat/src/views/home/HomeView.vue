<template>
  <div class="header">
    <div class="user-info">
      <el-avatar class="user-avatar" :src="user.avatar" />
      <div class="user-name">{{ user.username }}</div>
    </div>
    <div class="user-actions">
      <el-button @click="logout">Logout</el-button>
    </div>
  </div>
  <div class="home">
    <router-view></router-view>
    <div class="footer-router">
      <router-link to="/home/chatList">Chat List</router-link>
      <router-link v-if="lastRoom !== -1" :to="'/home/chat/' + lastRoom"
        >Chat</router-link
      >
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, provide, readonly, ref } from "vue";
import router from "@/router";
import axios from "@/plugins/axios";
import { ElMessage } from "element-plus";

interface User {
  id: number;
  username: string;
  avatar: string;
}

onMounted(() => {
  if (!localStorage.getItem("token")) {
    ElMessage.error("Please login first");
    router.push("/login");
  }
});

const user = ref({} as User);
const getUserInfo = () => {
  axios
    .get("/user/me")
    .then((res) => {
      console.log(res);
      user.value = res.data;
    })
    .catch((err) => {
      ElMessage.error(err.message);
    });
};
onMounted(getUserInfo);

const logout = () => {
  localStorage.removeItem("token");
  router.push("/");
};
const lastRoom = ref(-1);
const setLastRoom = (roomId: number) => {
  lastRoom.value = roomId;
};
provide("user", readonly(user));
provide("lastRoom", readonly(lastRoom));
provide("setLastRoom", setLastRoom);
</script>

<style scoped>
/* background */
.home {
  background-image: url("/public/bg.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 92vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 8vh;
  background-color: rgb(255, 255, 255);
}
.user-info {
  display: flex;
  align-items: center;
}
.user-avatar {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}
.footer-router {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 8vh;
}
.footer-router a:first-child {
  margin-right: 20px;
}
</style>
