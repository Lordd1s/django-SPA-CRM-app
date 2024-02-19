import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./AuthStore";

var auth = useAuthStore();

export const useCvStore = defineStore("CV", {
  state: () => ({
    loading: false,
    error: "",
    CVData: { length: 0 },
    howMuch: {},
    selectedCv: { length: 0 },
    short: true,
    slike: false,
    sdislike: false,
  }),

  actions: {
    async getCv() {
      this.loading = true;
      if (auth.getUser.isAdmin || auth.getUser.isStaff) {
        try {
          const response = await axios.get(
            "http://127.0.0.1:8000/all_cv_boss/",
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          //   console.log(response.data.length)
          console.log(response);
          if (response.status === 200) {
            if (response.data.length !== 0) {
              this.CVData = response.data;
              Object.assign(this.CVData, {length: response.data.length});
            }
            console.log(this.CVData);
          }
        } catch (error) {
          this.error = error;
          console.log(error);
        } finally {
          this.loading = false;
        }
      } else if (auth.getUser.isMaster) {
        try {
          const response = await axios.get("http://127.0.0.1:8000/all_cv/", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          });
          // console.log(response.data)
          if (response.status === 200) {
            this.CVData = response.data;
            Object.assign(this.CVData, { length: 1 });
            console.log(this.CVData);
          }
        } catch (error) {
          console.log(error);
          this.error = error;
        } finally {
          this.loading = false;
        }
      }
    },

    async download(period) {
      // console.log(period);
      let url = "";
      let fileName = "";
      try {
        this.loading = true;

        if (period === "today") {
          url = "http://127.0.0.1:8000/download_xlsx/period/today";
          fileName = "Резюме за сегодня.xlsx";
        } else if (period === "week") {
          url = "http://127.0.0.1:8000/download_xlsx/period/week";
          fileName = "Резюме за неделю.xlsx";
        } else if (period === "month") {
          url = "http://127.0.0.1:8000/download_xlsx/period/month";
          fileName = "Резюме за месяц.xlsx";
        } else if (period === null) {
          url = "http://127.0.0.1:8000/download_xlsx/period/allTime";
          fileName = "Резюме за все время.xlsx";
        } else if (Array.isArray(period) && period.length === 2) {
          const [start, end] = period;

          if (start && end) {
            url = `http://127.0.0.1:8000/download_xlsx/custom?startDate=${start}&endDate=${end}`;
            fileName = `Резюме за ${start} по ${end}.xlsx`;
          } else {
            console.error("Введите обе даты");
            return;
          }
        }

        const response = await axios.get(url, {
          responseType: "arraybuffer",
          headers: {
            "Content-Type":
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "Content-Disposition": `attachment; filename=${encodeURIComponent(
              fileName
            )}`,
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        // console.log(response.data)
        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        });
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
      } catch (error) {
        console.error(error);
        this.error = error;
        // console.log(url)
      } finally {
        this.loading = false;
      }
    },

    async getLike(cv) {
      this.loading = true;
      if (auth.getUser.isAdmin || auth.getUser.isStaff) {
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/cv_rate_get/${cv.id}/`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          if (response.status === 200) {
            console.log(response.data);
            this.howMuch = response.data;
          }
        } catch (error) {
          console.error(error);
        } finally {
          this.loading = false;
        }
      } else if (auth.getUser.isMaster) {
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/cv_rate_post/${this.selectedCv.id}/' '`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          if (response.status == 202) {
            this.slike = true;
            this.sdislike = true;
          } else if (response.status == 204) {
            this.slike = false;
            this.sdislike = false;
          }
        } catch (error) {
          this.error = error;
          console.error(error);
        } finally {
          this.loading = false;
        }
      }
    },

    async extend(cv) {
      this.short = !this.short;
      this.selectedCv = cv;
      Object.assign(this.selectedCv, { length: 1 });
      // console.log(this.selectedCv)
      this.loading = true;
      if (this.selectedCv.is_viewed === false) {
        try {
          await axios.put(`http://127.0.0.1:8000/cv/${cv.id}/`, cv, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          });
          this.selectedCv.is_viewed = true;
        } catch (error) {
          this.error = error;
          console.error(error);
        } finally {
          this.loading = false;
        }
      }
    },

    async like(cvId) {
      this.loading = true;
      try {
        await axios.post(
          `http://127.0.0.1:8000/cv_rate_post/${cvId}/true/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        alert("Успешно (Повторное нажатие не вызовет никаких изменений)!");
        this.slike = true;
        this.sdislike = true;
      } catch (error) {
        console.error(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async dislike(cvId) {
      this.loading = true;
      try {
        await axios.post(
          `http://127.0.0.1:8000/cv_rate_post/${cvId}/false/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        alert("Успешно (Повторное нажатие не вызовет никаких изменений)");
        this.sdislike = true;
        this.slike = true;
      } catch (error) {
        console.error(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async accept(cv) {
      this.loading = true;
      try {
        await axios.put(
          `http://127.0.0.1:8000/cv/${cv.id}/`,
          { is_accept: true },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        alert("Успешно принято");
        this.selectedCv.is_declined = false;
        this.selectedCv.is_accept = true;

        this.short = true;
      } catch (error) {
        this.error = error;
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async deleteCv(cv) {
      this.loading = true;
      try {
        const response = await axios.delete(
          `http://127.0.0.1:8000/cv/${cv.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          alert("Успешно удалено");
          this.short = true;
          if (this.selectedCv.length === 0) {
            this.short = false;
          }
          window.location.reload();
        }
      } catch (error) {
        this.error(error);
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async decline(cv) {
      this.loading = true;
      try {
        await axios.put(
          `http://127.0.0.1:8000/cv/${cv.id}/`,
          { is_declined: true },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        alert("Успешно отклонено!");
        this.selectedCv.is_declined = true;
        this.selectedCv.is_accept = false;

        this.short = true;
      } catch (error) {
        this.error = error;
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    shorten() {
      this.short = true;
    },

    getPhoto(photo) {
      return `http://127.0.0.1:8000${photo}`;
    },
  },

  getters: {
    getCVs() {
      return this.CVData;
    },

    getSelected() {
      return this.selectedCv;
    },

    getHowMuch() {
      return this.howMuch;
    },
  },
});
