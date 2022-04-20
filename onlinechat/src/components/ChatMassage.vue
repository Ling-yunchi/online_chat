<template>
  <div class="chat-massage">
    <div class="chat-massage__avatar">
      <el-avatar :size="45" fit="cover" :src="avatar" />
    </div>
    <div class="chat-massage__content">
      <div class="chat-massage__name">
        {{ name }}
        <span style="margin-left: 5px; font-weight: normal; font-size: 10px">{{
          new Date(Date.parse(time)).toISOString()
        }}</span>
      </div>
      <div class="chat-massage__text">{{ text }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatMassage",
  components: {},
  props: {
    avatar: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
    time: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.chat-massage {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 10px;
  background-color: #f5f5f5;
  margin-bottom: 10px;
}
.chat-massage__avatar {
  margin-right: 10px;
}
.chat-massage__content {
  display: flex;
  flex-direction: column;
}
.chat-massage__name {
  font-weight: bold;
  margin-bottom: 5px;
  text-align: left;
}
.chat-massage__text {
  text-align: left;
  max-width: 250px;
  word-break: break-word;
}
</style>
