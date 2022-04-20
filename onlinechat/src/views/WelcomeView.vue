<template>
  <div class="background">
    <div class="center">
      <div class="title">
        <h1>Online Chat</h1>
      </div>
      <div class="subtitle">
        <h2>completely anonymous chat online</h2>
      </div>
      <div class="button">
        <router-link to="/login">
          <el-button class="login">Login</el-button>
        </router-link>
        <router-link to="/register">
          <el-button class="register">Register</el-button>
        </router-link>
      </div>
    </div>
    <div class="about">
      <router-link to="/about">
        <el-link type="primary" :underline="false" style="font-weight: bold">
          About
        </el-link>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "WelcomeView",
};
</script>

<style scoped>
.background {
  background-image: url("/public/bg.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
}

.center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

a {
  text-decoration: none;
}

.title {
  font-size: 2em;
}

.subtitle {
  color: white;
}

.login {
  background-color: #2c3e50;
  color: white;
  width: 100px;
  height: 40px;
  border-radius: 20px;
  margin-right: 20px;
  font-weight: bold;
  border: 0;
}

.login:hover {
  background-color: #6dc2ef;
  color: white;
}

.register {
  background-color: #ffffff;
  color: #4ab1d5;
  width: 100px;
  height: 40px;
  border-radius: 20px;
  margin-right: 20px;
  font-weight: bold;
  border: 0;
}
.about {
  position: absolute;
  bottom: 20px;
  right: 50%;
}
</style>
