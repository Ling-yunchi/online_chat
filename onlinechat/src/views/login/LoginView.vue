<template>
  <div id="background">
    <div id="login-container">
      <div id="login-header">
        <h1>Online Chat</h1>
      </div>
      <div id="login-form">
        <el-form
          label-position="top"
          label-width="100px"
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginFormRules"
        >
          <el-form-item prop="username" :required="true" label="Username">
            <el-input
              v-model="loginForm.username"
              placeholder="Username"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password" :required="true" label="Password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="Password"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="login-btn" type="primary" @click="login">
              Login
            </el-button>
            <el-button
              class="register-btn"
              type="primary"
              @click="router.push('/register')"
            >
              Register
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import axios from "@/plugins/axios";
import { ElMessage, FormInstance } from "element-plus";
import router from "@/router";

const loginFormRef = ref<FormInstance>();
const loginForm = reactive({
  username: "",
  password: "",
});
const loginFormRules = reactive({
  username: [
    { required: true, message: "Username is required", trigger: "blur" },
    {
      min: 3,
      max: 10,
      message: "Username must be at least 3 and less than 10 characters",
      trigger: "blur",
    },
  ],
  password: [
    { required: true, message: "Password is required", trigger: "blur" },
    {
      min: 6,
      max: 20,
      message: "Password must be at least 6 and less than 20 characters",
      trigger: "blur",
    },
  ],
});
const login = async () => {
  console.log("login");
  if (!loginFormRef.value) return;
  let valid = await loginFormRef.value.validate();
  if (valid) {
    let form = new FormData();
    form.set("username", loginForm.username);
    form.set("password", loginForm.password);
    form.set("grant_type", "password");
    try {
      let res = await axios.post("/user/login", form, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
      if (res.status === 200) {
        localStorage.setItem("token", res.data.access_token);
        ElMessage.success("Login Success, Redirecting...");
        await router.push("/home");
      } else {
        ElMessage.error(res.data.message);
      }
    } catch (e: any) {
      ElMessage.error("Login Failed");
      return;
    }
  }
};
</script>

<style scoped>
#background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("/public/bg.png");
  background-size: cover;
  background-position: center;
}

#login-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 10px;
}

#login-header {
  position: relative;
  width: 100%;
  height: 50px;
}

#login-header h1 {
  text-align: center;
  font-size: 30px;
  font-weight: bold;
  color: #333;
}

#login-form {
  position: relative;
  width: 100%;
}

.login-btn {
  width: 100px;
  height: 30px;
  margin-top: 10px;
  margin-left: 20px;
  border-radius: 15px;
  border: 0;
}
.register-btn {
  width: 100px;
  height: 30px;
  margin-top: 10px;
  margin-left: 30px;
  border-radius: 15px;
  border: 0;
}
</style>
