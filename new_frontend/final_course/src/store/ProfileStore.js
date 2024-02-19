import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useAuthStore } from "./AuthStore";

var AuthStore = useAuthStore().getUser;

export const useProfileStore = defineStore("profile", {
  state: () => ({
    error: ref(null),
    loading: false,
    profile: { length: 0 },
    avatar: ref(null),
  }),
  actions: {
    async getProfileFromBack() {
      this.loading = true;
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/profile/?userId=${AuthStore.id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.profile = response.data;
          this.avatar = response.data.avatar;
          Object.assign(this.profile, { length: 1 });
          localStorage.setItem("profile", JSON.stringify(this.profile));
        } else if (response.status === 404) {
          this.error = response.data;
        }
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async sendUpdProfile(updForm) {
      this.loading = true;
        console.log(updForm);
      const headers = {
        "Content-Type": "multipart/form-data; charset=utf-8",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      };

      try {
        const response = await axios.patch(
          `http://127.0.0.1:8000/profile/?userId=${AuthStore.id}`,
          updForm,
          { headers }
        );

        if (response.status === 201) {
          const updatedFields = Object.keys(updForm).filter(
            (field) => updForm[field]
          );
          updatedFields.forEach((field) => {
            if (field === "avatar") {
              this.avatar = updForm.avatar;
            } else {
              this.profile[field] = updForm[field];
            }
          });

          window.location.reload();
        } else if (response.status === 400) {
          this.error = "Заполните хотя бы одно поле!";
        }
      } catch (error) {
        console.error(error);
        this.error = error.message || "Ошибка при обновлении профиля";
      } finally {
        this.loading = false;
      }
    },
  },

  restoreProfile() {
    const data = localStorage.getItem("profile");
    if (data) {
      this.profile = data;
    }
  },
  getters: {
    getProfile() {
      return this.profile;
    },

    getAvatar() {
      return `http://127.0.0.1:8000${this.avatar}`;
    },
  },
});
