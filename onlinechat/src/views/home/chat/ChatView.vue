<template>
  <el-card class="box-card chat-container">
    <div class="chat-header">
      <div class="chat-title">
        <span style="margin-right: 250px">{{ roomInfo.name }}</span>
        <el-button type="text" icon="el-icon-close" @click="closeChat"
          >exit</el-button
        >
      </div>
    </div>
    <div id="chat-view">
      <el-scrollbar ref="scrollbarRef">
        <div class="chat-list" v-for="item in resultMessage" :key="item.id">
          <chat-message
            :text="item.message"
            :name="item.username"
            :time="item.time"
            :avatar="item.avatar"
          />
        </div>
      </el-scrollbar>
    </div>
    <div>
      <el-popover
        placement="top"
        title="表情"
        width="500"
        height="500"
        trigger="click"
      >
        <template #reference>
          <el-button class="emoji-button">😀</el-button>
        </template>
        <el-scrollbar>
          <div class="emoji-list">
            <el-row :gutter="1">
              <el-col :span="1" v-for="(item, index) in faceList" :key="index">
                <el-button type="text" size="small" @click="getBrow(index)">
                  {{ item }}
                </el-button>
              </el-col>
            </el-row>
          </div>
        </el-scrollbar>
      </el-popover>
      <el-button
        class="submit-btn"
        type="primary"
        @click="
          sendMessage(content);
          content = '';
        "
        :disabled="content === ''"
        >发送
      </el-button>
      <el-input
        :rows="5"
        type="textarea"
        placeholder="请输入内容"
        resize="none"
        v-model="content"
      >
      </el-input>
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { defineProps, inject, onMounted, onUnmounted, ref } from "vue";
import ChatMessage from "@/components/ChatMassage.vue";

import emojis from "@/assets/emoji.json";
import io from "socket.io-client";
import axios from "@/plugins/axios";
import router from "@/router";
import { ElMessage, ElScrollbar } from "element-plus";

const props = defineProps<{
  roomId: string;
}>();

interface RoomInfo {
  id: number;
  name: string;
  create_time: string;
  create_user_id: string;
  description: string;
  online_num: number;
}

const roomInfo = ref({} as RoomInfo);
const getRoomInfo = () => {
  console.log();
  axios
    .get(`/chat/room/${props.roomId}`)
    .then((res) => {
      roomInfo.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};
onMounted(getRoomInfo);

const closeChat = () => {
  disconnect();
  router.push("/home/chatList");
};

const content = ref(""); //聊天输入内容
const faceList = ref([] as string[]); //表情列表
const getBrowString = ref(""); //表情文本
const getBrow = (idx: number) => {
  for (let i in faceList.value) {
    if (idx === parseInt(i)) {
      getBrowString.value = faceList.value[idx];
      content.value += getBrowString.value;
    }
  }
};
const loadEmoji = () => {
  for (let i in emojis) {
    faceList.value.push(emojis[i as keyof typeof emojis].char);
  }
};
onMounted(loadEmoji);

interface ChatMessageItem {
  id: number;
  user_id: number;
  username: string;
  avatar: string;
  message: string;
  time: string;
}

const user: any = inject("user");

const resultMessage = ref([] as ChatMessageItem[]);
const loadMessage = () => {
  axios
    .get(`/chat/room/${props.roomId}/messages`)
    .then((res) => {
      console.log(res);
      console.log(res.data);
      resultMessage.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};
onMounted(loadMessage);

const scrollbarRef = ref<InstanceType<typeof ElScrollbar>>();

const socket = ref(
  io("https://www.topquant.tech", {
    path: "/wr_web/data/socket.io",
    autoConnect: false,
    reconnection: true,
    auth: {
      token: "Bearer " + localStorage.getItem("token"),
    },
  })
);
socket.value.on("connect", () => {
  console.log("connected");
  socket.value.emit("enter_room", props.roomId);
});
socket.value.on("disconnect", () => {
  console.log("disconnected");
});
socket.value.on("enter_room", (data: any) => {
  console.log(data);
});
socket.value.on("room_info", (msg: string) => {
  console.log(msg);
  ElMessage.info(msg);
});
socket.value.on("room_message", (msg: ChatMessageItem) => {
  console.log(msg);
  //push front
  resultMessage.value.unshift(msg);
});
socket.value.on("errorMessage", (err: any) => {
  console.log(err);
  ElMessage.error(err);
});
socket.value.on("error", (err: any) => {
  console.log(err);
  ElMessage.error(err);
});
const connectSocket = () => {
  if (socket.value.disconnected) {
    socket.value.connect();
  }
};
const sendMessage = (msg: string) => {
  socket.value.emit("send_message", {
    user_id: user.value.id,
    room_id: roomInfo.value.id,
    message: msg,
  });
};
const disconnect = () => {
  socket.value.emit("leave_room", roomInfo.value.id);
  socket.value.disconnect();
};
onMounted(connectSocket);
onUnmounted(disconnect);

// before user close the page or refresh the page ,we need to disconnect the socket
window.addEventListener("unload", disconnect);
</script>

<style scoped>
.chat-container {
  width: 400px;
  height: 550px;
  padding: 0;
  margin: 0;
}

.chat-title {
  padding: 0;
  margin: 0;
  font-weight: bold;
  font-size: 20px;
}

.submit-btn {
  margin: 0 15px 10px 0;
  float: right;
}

#chat-view {
  height: 300px;
  background: #f5f5f5;
  border-radius: 10px;
  margin-bottom: 10px;
}

.emoji-list {
  max-width: 450px;
}

.emoji-button {
  float: left;
}
</style>
