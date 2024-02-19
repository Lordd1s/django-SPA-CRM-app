import { defineStore } from "pinia";
import { parseJwt } from "./Decoder";
import { ref } from "vue";
import axios from "axios";
import router from "@/router/index";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    error: ref(null),
    loading: false,
    message: ref(null),
    userInfo: { length: 0 },
  }),

  actions: {
    async authentificate(username, password) {
      this.loading = true;
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/token/",
          {
            username: username,
            password: password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (response.status === 200) {
          localStorage.setItem("accessToken", response.data.access);
          localStorage.setItem("refreshToken", response.data.refresh);

          this.setInfo();
          this.message = "Successfully";
          router.push({ name: "Home" });
        } else if (response.status === 401) {
          this.error = "Неверный логин или пароль!";
        }
      } catch (error) {
        console.error("Authentication failed:", error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async registrate(username, password, email) {
      try {
        const request = await axios.post(
          "http://127.0.0.1:8000/registrate/",
          {
            username: username,
            password: password,
            email: email,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        // console.log(request);
        if (request.status === 201) {
          this.message = "Регистрация прошла успешно! Можете войти в систему!";
        } else if (request.status === 400) {
          this.error = "Не все поля заполнены!";
        } else if (request.status === 406) {
          this.error = "Пользователь с таким email существует!";
        } else if (request.status === 403) {
          this.error = "Не правильный email или пароль!";
        }
      } catch (error) {
        this.error = error;
      } finally {
        rout.push({ name: "Login" });
      }
    },

    async setInfo() {
      this.loading = true;
      if (localStorage.getItem("accessToken")) {
        var token = localStorage.getItem("accessToken");
      }

      const tokenPayload = parseJwt(token);
      // console.log(tokenPayload);
      try {
        const request = await axios.get(
          `http://127.0.0.1:8000/login/${tokenPayload.user_id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (request.status == 200) {
          console.log(request);
          this.userInfo = request.data;
          for (let index = 0; index < request.data.groups.length; index++) {
            let group = request.data.groups[index];
            switch (group) {
              case 1:
                Object.assign(this.userInfo, { isAdmin: true });
                break;
              case 2:
                Object.assign(this.userInfo, { isMaster: true });
                break;
              case 3:
                Object.assign(this.userInfo, { isStaff: true });
                break;
              case 4:
                Object.assign(this.userInfo, { isMaster: true });
                break;
              default:
                break;
            }
          }

          Object.assign(this.userInfo, { length: 1 });

          localStorage.setItem("userInfo", JSON.stringify(this.userInfo));
          // console.log(this.userInfo);
        }
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    restoreUserInfo() {
      const savedData = localStorage.getItem("userInfo");
      if (savedData) {
        this.userInfo = JSON.parse(savedData);
      }
    },

    logout() {
      console.log("logout");
      this.userInfo = ref({ length: 0 });
      localStorage.removeItem("userInfo");
      localStorage.removeItem("profile");
      router.push({ name: "Login" });
    },
  },

  getters: {
    getUser() {
      return this.userInfo;
    },
  },
});
