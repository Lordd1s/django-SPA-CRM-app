import { createPinia, defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";
import { parseJwt } from "../components/AppHeader.vue";

const pinia = createPinia();

export const authStore = defineStore({
  id: "authStore",
  state: () => ({
    username: ref(null),
    isAdmin: ref(null),
    isStaff: ref(null),
    isMaster: ref(null),
    userId: ref(null),
  }),
  actions: {
    async login() {
      if (localStorage.getItem("accessToken")) {
        var accessToken = localStorage.getItem("accessToken");
      }

      // Декодируем токен и получаем id пользователя
      const tokenPayload = parseJwt(accessToken);
      this.userId = tokenPayload.user_id;

      if (tokenPayload) {
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/login/${tokenPayload.user_id}/`,
            {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            }
          );

          if (response.data.groups.length > 0) {
            this.isMaster = true;
          }
          if (response.data.is_staff) {
            this.isStaff = true;
          }
          if (response.data.is_superuser) {
            this.isAdmin = true;
          }
          if (this.isAdmin && this.isStaff) {
            this.isMaster = false;
          }
          this.username = response.data.username;
        } catch (error) {
          this.username = null;
        }
      }
    },
    setUsername(value) {
      this.username = value;
    }
  },
});

export const profile = defineStore({
  id: "profile",
  state: () => ({
    prof: ref(null),
  }),
  actions: {
    addData(profile) {
      this.prof.push(profile);
    }
  }
});

export const chatMessage = defineStore({
  id: "chatMessage",
  state: () => ({
    messages: ref([]),
  }),
  actions: {
    addMessage(message) {
      this.messages.push(message);
    }
  }
});

export const useChat = defineStore({
  id: "useChat",
  state: () => ({
    username: ref(null),
    chat_groups: ref(null),
    error: ref([]),
    loading: false,
  }),
  actions: {
    async getGroups() {
      this.loading = true;
      try {
        const res = await axios.get("http://127.0.0.1:8000/chat_groups/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        if (res.status === 200) {
          this.chat_groups = res.data;
          this.username = this.chat_groups.private[0].owner.username;
          console.log(this.chat_groups)
        }
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
  },
});
