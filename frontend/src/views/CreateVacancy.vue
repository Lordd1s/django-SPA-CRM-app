<template>
    <div class="size mt-5">
        <div class="form-control my-3"  v-if="isAdmin">
        <form @submit.prevent="createVacancy">
            <label class="form-label mt-3">Должность</label>
            <input type="text" class="form-control" v-model="vacancy.title">

            <label class="form-label mt-3">Описание</label>
            <textarea type="text" class="form-control" v-model="vacancy.description"></textarea>

            <label class="form-label mt-3">Требуемый персонал</label>
            <input type="number" class="form-control" v-model="vacancy.required_person">

            <button class="btn btn-outline-primary form-control mt-3">Отправить</button>
        </form>
    </div>

    <div class="text-center" v-else>
        <h1 class="h1 my-4">У вас нет прав создать вакансию</h1>
    </div>
    </div>
    
</template>

<script>
import { authStore } from "@/store/store";
import axios from "axios";
import { parseJwt } from "@/components/AppHeader.vue";
import router from "@/router/router";

export default {
    setup() {
        const isAdmin = authStore().isAdmin;

        return { isAdmin }
    },
    
    data() {
        return {
            vacancy: {
                title: '',
                description: '',
                required_person: null
            }
        }
    },
    async mounted() {
        await this.checkStaff()
    },

    methods: {
        async checkStaff() {
            const token = parseJwt(localStorage.getItem('accessToken'))
            try {
                const response = await axios.get(`http://127.0.0.1:8000/login/${token.user_id}/`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    });
                if (response.data.groups.length > 0) {
                    this.isAdmin = true;
                }
            } catch (error) {
                console.error(error);
                alert('У вас нету прав создать вакансию! Если вы хотите создать вакансию, обращайтесь к администратору');
                this.$router.push({name: 'Home'})
            }
        },

        async createVacancy() {
            try {
                await axios.post(`http://127.0.0.1:8000/cud_vacancy/' '/`, this.vacancy, 
                {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                    }
                })
                alert('Вакансия успешно создана');
                this.$router.push({name: 'Vacancy'});
            } catch (error) {
                console.error(error);
                alert('Error: ' + error)
            }
        }
    }


}
</script>

<style scoped>
.size {
    width: 40%;
    border-radius: 5px;
    box-shadow: 0 0 10px;
    padding: 2%;
    margin: auto;
    background: whitesmoke;
}
</style>