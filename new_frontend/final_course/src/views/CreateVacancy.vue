<template>
    <div class="size mt-5">
        <div :class="modalShowLoading" id="exampleModalCenter" tabindex="-1" aria-labelledby="exampleModalCenterTitle"
            aria-modal="true" role="dialog" style="display: block;" v-if="vac.loading">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">Выполняется запрос...</h3>
                        <div class="spinner-border spinner-border-sm" role="status">
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div :class="modalShowError" id="exampleModalCenter" tabindex="-1" aria-labelledby="exampleModalCenterTitle"
            aria-modal="true" role="dialog" style="display: block;" v-if="vac.error">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">Ошибка!</h3>
                    </div>
                    <div class="modal-title">
                        <p class="modal-title">{{vac.error}}</p>
                    </div>

                </div>
            </div>
        </div>
        <div class="form-control my-3" v-if="auth.getUser.isAdmin">
            <form @submit.prevent="vac.createVacancy(vacancy)">
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
import { useAuthStore } from "@/store/AuthStore";
import { useVacancyCreate } from "@/store/VacancyStore";



export default {
    setup() {
        const authStores = useAuthStore();
        const vacancyCreate = useVacancyCreate();

        return { auth: authStores, vac: vacancyCreate }
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

    methods: {
        modalShowError() {
            if (this.vacancy.error) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },
        modalShowLoading() {
            if (this.vacancy.loading) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },


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