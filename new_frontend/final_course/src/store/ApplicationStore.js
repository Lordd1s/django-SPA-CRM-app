import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./AuthStore";

var auth = useAuthStore();

export const useBidStore = defineStore("BidStore", {
  state: () => ({
    loading: false,
    error: "",
    bidData: { length: 0 },
    showBid: false,
    data: { length: 0 },
  }),

  actions: {
    async getApplications() {
      this.loading = true;
      if (auth.getUser.isAdmin || auth.getUser.isStaff) {
        try {
          const rs = await axios.get(
            "http://127.0.0.1:8000/applications/solution",
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          if (rs.status === 200) {
            this.data = rs.data;
            Object.assign(this.data, { length: rs.data.length });
          }
        } catch (error) {
          console.error(error);
          this.error = error;
        } finally {
          this.loading = false;
        }
      } else if (auth.getUser.isMaster) {
        return null;
      }
    },

    async getBid() {
      this.loading = true;
      try {
        const res = await axios.get("http://127.0.0.1:8000/application/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        if (res.status === 200) {
          this.bidData = res.data;
          Object.assign(this.bidData, { length: this.bidData.length });
        }
        console.log(res.data);
      } catch (error) {
        console.error(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async sendBid(bid) {
      this.loading = true;
      try {
        await axios.post("http://127.0.0.1:8000/application/", bid, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        alert("Заявка успешно отправлена!");
      } catch (error) {
        console.error(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async sendApplicationStatus(st) {
      const [pk, status] = st;
      this.loading = true;
      try {
        await axios.patch(
          `http://127.0.0.1:8000/applications/solution?status=${status}&pk=${pk}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        window.location.reload();
      } catch (error) {
        console.error(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
  },

  getters: {
    getBidData() {
      return this.bidData;
    },

    getDataAccepted() {
      return this.data.filter(b => b.is_accepted === "1");
    },
    getDataDeclined() {
      return this.data.filter(b => b.is_accepted === "0")
    },
    getDataNotViewed() {
      return this.data.filter(b => b.is_accepted === "2")
    },
    getAllData() {
      return this.data
    },


    changeShow() {
      this.showBid = !this.showBid;
    }
  },
});
