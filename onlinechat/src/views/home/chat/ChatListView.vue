<template>
  <el-card class="container">
    <el-row>
      <el-col :span="16" style="margin-bottom: 10px">
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
          <el-table-column prop="id" label="ID" width="70" sortable>
            <template v-slot="scope">
              <el-popover
                v-if="scope.row.create_user_id === user?.id"
                placement="right"
                style="background-color: rgba(255, 181, 181, 0)"
              >
                <template #default v-if="scope.row.create_user_id === user?.id">
                  <span style="font-weight: bold; margin-right: 10px">{{
                    scope.row.name
                  }}</span>
                  <el-button
                    type="primary"
                    :icon="Edit"
                    circle
                    @click="
                      editRoomDialogVisible = true;
                      editingRoomInfo = scope.row;
                    "
                  />
                  <el-button
                    type="danger"
                    :icon="Delete"
                    circle
                    @click="deleteRoom(scope.row.id)"
                  />
                </template>
                <template #reference>
                  <div style="font-weight: bold; width: 100%">
                    *{{ scope.row.id }}
                  </div>
                </template>
              </el-popover>
              <div v-else>{{ scope.row.id }}</div>
            </template>
          </el-table-column>
          <el-table-column
            prop="name"
            label="Name"
            width="80"
          ></el-table-column>
          <el-table-column
            prop="created_time"
            label="Create Time"
            width="160"
            sortable
          ></el-table-column>
          <el-table-column
            prop="description"
            label="Description"
            width="300"
          ></el-table-column>
          <el-table-column
            prop="online_num"
            label="Visit Num"
            width="90"
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
      <el-button type="primary" @click="createChatRoom"> Create</el-button>
      <el-button type="info" @click="createRoomDialogVisible = false">
        Cancel
      </el-button>
    </div>
  </el-dialog>

  <!-- edit room dialog -->
  <el-dialog
    :title="`Edit Chat Room`"
    v-model="editRoomDialogVisible"
    width="50%"
  >
    <el-form
      :model="editRoomForm"
      ref="editRoomFormRef"
      :rules="editRoomFormRule"
    >
      <el-form-item label="Name" prop="name">
        <el-input
          required
          v-model="editRoomForm.name"
          placeholder="Name"
        ></el-input>
      </el-form-item>
      <el-form-item label="Description" prop="description">
        <el-input
          type="textarea"
          v-model="editRoomForm.description"
          placeholder="Description"
        ></el-input>
      </el-form-item>
    </el-form>
    <div class="edit-room-dialog-footer">
      <el-button type="primary" @click="editRoom"> Edit</el-button>
      <el-button type="info" @click="editRoomDialogVisible = false">
        Cancel
      </el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { Edit, Delete } from "@element-plus/icons-vue";
import { inject, onMounted, reactive, Ref, ref } from "vue";
import axios from "@/plugins/axios";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import router from "@/router";
import moment from "moment";

interface User {
  id: number;
  username: string;
  avatar: string;
}

const user: Ref<User> | undefined = inject("user");
const setLastRoom: any = inject("setLastRoom");

interface ChatRoom {
  id: string;
  name: string;
  create_user_id: number;
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
      // check data id is existed
      let data: ChatRoom[] = res.data;
      data.forEach((data) => {
        data.created_time = moment(data.created_time)
          .utcOffset("+16:00")
          .format("YYYY-MM-DD HH:mm:ss");
      });
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
    console.log(user?.value);
    axios
      .post("/chat/room", {
        ...createRoomForm.value,
        create_user_id: user?.value.id,
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

const editRoomFormRef = ref<FormInstance>();
const editRoomForm = ref({
  name: "",
  description: "",
});
const editRoomFormRule = reactive({
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
const editRoomDialogVisible = ref(false);
const editingRoomInfo = ref<ChatRoom>();
const editRoom = async () => {
  if (!editRoomFormRef.value) return;
  if (await editRoomFormRef.value.validate()) {
    axios
      .put(`/chat/room/${editingRoomInfo.value?.id}`, {
        ...editRoomForm.value,
        create_user_id: user?.value.id,
      })
      .then((res) => {
        ElMessage.success(res.data.msg);
        editRoomDialogVisible.value = false;
        editRoomFormRef.value?.resetFields();
        searchChatRoom(1);
      })
      .catch((err) => {
        ElMessage.error(err.message);
      });
  }
};
const deleteRoom = (roomId: number) => {
  ElMessageBox.confirm("Are you sure to delete this room?")
    .then(() => {
      axios
        .delete(`/chat/room/${roomId}`)
        .then((res) => {
          ElMessage.success(res.data.msg);
          searchChatRoom(1);
        })
        .catch((err) => {
          ElMessage.error(err.message);
        });
    })
    .catch(() => {
      // do nothing
    });
};
</script>

<style scoped>
.container {
  height: 80%;
  overflow: hidden;
}
</style>
