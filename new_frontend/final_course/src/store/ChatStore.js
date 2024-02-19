import axios from "axios";
import { defineStore } from "pinia";

export const useChatStore = defineStore("useChatStore", {
  state: () => ({
    loading: false,
    error: "",
    groups: {
      public: [],
      private: [],
    },
    showCreateForm: false,
  }),

  actions: {
    async getGroupsOnBack() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/chat_groups", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        if (response.status === 200) {
          this.groups.private = response.data.private;
          this.groups.public = response.data.public;
        }
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async createGroup() {
        this.loading = true;
      try {
        const request = await axios.post(
          "http://127.0.0.1:8000/create_group/",
          {
            name: this.group_name_post,
            is_private_checkbox: this.is_private_checkbox,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (request.status == 201) {
          alert("Успешно создано!");
          this.showCreateForm = !this.showCreateForm;
          window.location.reload();
        } else if (request.status == 400) {
          alert(
            "Заполните поле или неправильное имя! Имя группы должен состоять из английских букв и цифры! Минимальная длина 4"
          );
        }
      } catch (error) {
        console.error(error);
        alert("Ошибка!");
      } finally {
        this.loading = false;
      }
    },
  },

  getters: {
    getPubs() {
      return this.groups.public;
    },

    getPriv() {
      return this.groups.private;
    },
  },
});

export const useChatMessage = defineStore(
    'ChatMessage',
    {
        state: () => ({
            loading: false,
            error: ''
            
        })
    }
)