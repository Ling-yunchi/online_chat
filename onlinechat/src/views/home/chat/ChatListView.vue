<template>
  <el-card class="container">
    <el-row>
      <el-col :span="16">
        <el-input
          v-model="search"
          placeholder="Search"
          size="small"
          @keyup.enter="searchChatRoom(1)"
        >
        </el-input>
      </el-col>
      <el-col :span="4">
        <el-button
          style="width: 100%"
          type="primary"
          size="small"
          @click="searchChatRoom(1)"
        >
          Search
        </el-button>
      </el-col>
      <el-col :span="4">
        <el-button
          style="width: 100%"
          type="success"
          size="small"
          @click="createRoomDialogVisible = true"
        >
          Create
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-table
          :data="chatList"
          highlight-current-row
          border
          height="480px"
          style="width: 100%"
          @row-click="handleSelect"
        >
          <el-table-column prop="id" label="ID" width="50"></el-table-column>
          <el-table-column
            prop="name"
            label="Name"
            width="80"
          ></el-table-column>
          <el-table-column
            prop="created_time"
            label="Create Time"
            width="150"
          ></el-table-column>
          <el-table-column
            prop="description"
            label="Description"
            width="300"
          ></el-table-column>
          <el-table-column
            prop="online_num"
            label="Visit Num"
            width="110"
          ></el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </el-card>

  <!-- create room dialog -->
  <el-dialog
    title="Create Chat Room"
    v-model="createRoomDialogVisible"
    width="50%"
  >
    <el-form
      :model="createRoomForm"
      ref="createRoomFormRef"
      :rules="createRoomFormRule"
    >
      <el-form-item label="Name" prop="name">
        <el-input
          required
          v-model="createRoomForm.name"
          placeholder="Name"
        ></el-input>
      </el-form-item>
      <el-form-item label="Description" prop="description">
        <el-input
          type="textarea"
          v-model="createRoomForm.description"
          placeholder="Description"
        ></el-input>
      </el-form-item>
    </el-form>
    <div class="create-room-dialog-footer">
      <el-button type="primary" @click="createChatRoom"> Create </el-button>
      <el-button type="info" @click="createRoomDialogVisible = false">
        Cancel
      </el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { inject, onMounted, reactive, ref } from "vue";
import axios from "@/plugins/axios";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import router from "@/router";
const user: any = inject("user");
const setLastRoom: any = inject("setLastRoom");

interface ChatRoom {
  id: string;
  name: string;
  description: string;
  created_time: string;
  online_num: number;
}
const search = ref("");
const nowPage = ref(1);
const chatList = ref<ChatRoom[]>([]);
const searchChatRoom = (page: number) => {
  if (page === 1) {
    nowPage.value = 1;
  } else {
    nowPage.value = page;
  }
  axios
    .get("/chat/rooms", {
      params: {
        name: search.value,
        page: page,
        page_size: 1000,
      },
    })
    .then((res) => {
      // check data id is exist
      const data = res.data;
      chatList.value = data;
    })
    .catch((err) => {
      ElMessage.error(err.message);
    });
};
onMounted(() => {
  searchChatRoom(1);
});

const handleSelect = (row: ChatRoom, column: any, event: any) => {
  ElMessageBox.confirm(`confirm enter room ${row.name}?`)
    .then(() => {
      setLastRoom(row.id);
      router.push(`/home/chat/${row.id}`);
    })
    .catch(() => {
      // do nothing
    });
};

const createRoomFormRef = ref<FormInstance>();
const createRoomForm = ref({
  name: "",
  description: "",
});
const createRoomFormRule = reactive({
  name: [
    { required: true, message: "Please input name", trigger: "blur" },
    {
      min: 2,
      max: 20,
      message: "Length must be between 2 and 20",
      trigger: "blur",
    },
  ],
  description: [
    { required: true, message: "Please input description", trigger: "blur" },
    {
      min: 2,
      max: 100,
      message: "Length must be between 2 and 100",
      trigger: "blur",
    },
  ],
});
const createRoomDialogVisible = ref(false);
const createChatRoom = async () => {
  if (!createRoomFormRef.value) return;
  if (await createRoomFormRef.value.validate()) {
    console.log(user.value);
    axios
      .post("/chat/room", {
        ...createRoomForm.value,
        create_user_id: user.value.id,
      })
      .then((res) => {
        ElMessage.success(res.data.msg);
        createRoomDialogVisible.value = false;
        createRoomFormRef.value?.resetFields();
        searchChatRoom(1);
      })
      .catch((err) => {
        ElMessage.error(err.message);
      });
  }
};
</script>

<style scoped>
.container {
  height: 80%;
  overflow: auto;
}
</style>
