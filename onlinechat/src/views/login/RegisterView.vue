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
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerFormRules"
        >
          <el-form-item prop="username" :required="true" label="Username">
            <el-input
              v-model="registerForm.username"
              placeholder="Username"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password" :required="true" label="Password">
            <el-input
              v-model="registerForm.password"
              type="password"
              show-password
              placeholder="Password"
            ></el-input>
          </el-form-item>
          <el-form-item prop="avatar" :required="false" label="Avatar URL">
            <el-avatar
              :size="45"
              fit="cover"
              :src="registerForm.avatar"
            ></el-avatar>
            <el-input
              style="margin-top: 10px"
              v-model="registerForm.avatar"
              placeholder="Avatar URL"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="register-btn" type="primary" @click="register">
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

const registerFormRef = ref<FormInstance>();
const registerForm = reactive({
  username: "",
  password: "",
  avatar: "",
});
const validateUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error("Username is required."));
  } else if (value.length < 3) {
    callback(new Error("Username must be at least 3 characters."));
  } else if (value.length > 15) {
    callback(new Error("Username must be less than 15 characters."));
  } else {
    axios
      .get("/user/username", {
        params: {
          username: value,
        },
      })
      .then((res) => {
        if (res.data.exists) {
          console.log(res.data.exists);
          callback(new Error("Username already exists."));
        } else {
          callback();
        }
      })
      .catch((err) => {
        callback(new Error("Username already exists."));
      });
  }
};
const registerFormRules = reactive({
  username: [
    { required: true, message: "Username is required", trigger: "blur" },
    { validator: validateUsername, trigger: "blur" },
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
  avatar: [
    {
      required: false,
      trigger: "blur",
    },
  ],
});
const register = async () => {
  if (!registerFormRef.value) return;
  let valid = await registerFormRef.value.validate();
  if (valid) {
    try {
      let res = await axios.post("/user/register", {
        username: registerForm.username,
        password: registerForm.password,
        avatar: registerForm.avatar,
      });
      if (res.status === 200) {
        ElMessage.success("Register Success, Redirecting...");
        await router.push("/login");
      } else {
        ElMessage.error(res.data.message);
      }
    } catch (e: any) {
      ElMessage.error("Register Failed");
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
