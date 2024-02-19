<template>
    <main>
        <!-- Форма для отправки резюме! -->
        <section v-if="vacancy.showForm"> 
            <CVPost /> 
        </section>

        <!-- Вакансии! -->
        <section v-else>
            <div class="text-center my-3" v-if="!vacancy.vacancyData">
                <span class="h1">Нет доступных вакансии</span>
            </div>

            <div v-if="vacancy.showVac">
                <div class="form-floating size mt-4">
                    <input type="text" v-model="searchQuery" class="form-control" placeholder="Поиск по вакансиям">
                    <label>Поиск по вакансиям</label>
                </div>

                <div class="container mt-4" v-if="searchQuery">
                    <div class="card mx-auto my-3 p-3" v-for="vac in filteredVacancies" :key="vac.id">
                        <h3 class="h3 card-header" style="background-color: #27343c; color: #fff;">{{ vac.title }}</h3>
                        <div class="card-body" style="background-color: #546e7a; color: #fff;">
                            <p v-if="vac.is_active" class="mb-3"><strong>Статус:</strong> Активно</p>
                            <p v-else class="mb-3"><strong>Статус:</strong> Не активно</p>
                            <p class="mb-3"><strong>Описание:</strong> {{ vac.description }}</p>
                        </div>
                        <div class="card-footer d-flex justify-content-between"
                            style="background-color: #27343c; color: #fff;">
                            <div>
                                <p class="mb-1"><strong>Требуемый персонал:</strong> {{ vac.required_person }}</p>
                                <span><strong>Выложено:</strong> {{ vac.date_created }}</span>
                            </div>
                            <div class="custom-buttons">
                                <button class="btn custom-btn primary disabled"
                                    v-if="auth.isAdmin || auth.isStaff || auth.isMaster">Откликнуться</button>
                                <button class="btn custom-btn danger" v-if="auth.isAdmin || auth.isStaff"
                                    @click="deleteVacancy(vac)">Удалить</button>
                                <button class="btn custom-btn warning" v-if="auth.isAdmin || auth.isStaff"
                                    @click="changeVacancy(vac)">Редактировать</button>
                                <button class="btn custom-btn primary" v-if="auth.username === null"
                                    @click="show">Откликнуться</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="container mt-4" v-else>
                    <div class="card mx-auto my-3 p-3" v-for="vac in vacancy.getVacancyData" :key="vac.id">
                        <h3 class="h3 card-header" style="background-color: #27343c; color: #fff;">{{ vac.title }}</h3>
                        <div class="card-body" style="background-color: #546e7a; color: #fff;">
                            <p v-if="vac.is_active" class="mb-3"><strong>Статус:</strong> Активно</p>
                            <p v-else class="mb-3"><strong>Статус:</strong> Не активно</p>
                            <p class="mb-3"><strong>Описание:</strong> {{ vac.description }}</p>
                        </div>
                        <div class="card-footer d-flex justify-content-between"
                            style="background-color: #27343c; color: #fff;">
                            <div>
                                <p class="mb-1"><strong>Требуемый персонал:</strong> {{ vac.required_person }}</p>
                                <span><strong>Выложено:</strong> {{ vac.date_created }}</span>
                            </div>
                            <div class="custom-buttons">
                                <button class="btn custom-btn primary disabled"
                                    v-if="auth.getUser.isAdmin || auth.getUser.isStaff || auth.getUser.isMaster">Откликнуться</button>
                                <button class="btn custom-btn danger" v-if="auth.getUser.isAdmin || auth.getUser.isStaff"
                                    @click="vacancy.deleteVacancy(vac)">Удалить</button>
                                <button class="btn custom-btn warning" v-if="auth.getUser.isAdmin || auth.getUser.isStaff"
                                    @click="changeVacancy(vac)">Редактировать</button>
                                <button class="btn custom-btn primary" v-if="auth.getUser.length === 0"
                                    @click="show">Откликнуться</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="size upd mt-5" v-if="showChange">
                <div :class="modalShowSuccess" id="exampleModalCenter" tabindex="-1"
                    aria-labelledby="exampleModalCenterTitle" aria-modal="true" role="dialog" style="display: block;"
                    v-if="vacancy.message">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h3 class="modal-title">Успешно обновлено, можете вернуться назад!</h3>
                            </div>
                        </div>
                    </div>
                </div>
                <form @submit.prevent="vacancy.updVac(changedVacancy)">
                    <label class="form-label mt-3">Должность</label>
                    <input type="text" class="form-control" v-model="changedVacancy.title">

                    <label class="form-label mt-3">Описание</label>
                    <textarea type="text" class="form-control" v-model="changedVacancy.description"></textarea>

                    <label class="form-label mt-3">Требуемый персонал</label>
                    <input type="number" class="form-control" v-model="changedVacancy.required_person">

                    <label class="form-label mt-3">Активно ли вакансия</label>
                    <br>
                    <input type="checkbox" v-model="changedVacancy.is_active">

                    <button class="btn btn-outline-primary form-control mt-3">Отправить</button>
                </form>
                <button class="btn btn-outline-secondary form-control mt-3" @click="showVacancy">Вернуться к
                    вакансиям</button>
            </div>
        </section>

    </main>
</template>

<script>
import { defineComponent, onMounted } from 'vue';
import { useAuthStore } from '@/store/AuthStore';
import { useVacancyStore } from '@/store/VacancyStore';
import CVPost from '@/components/CVPost.vue';


export default defineComponent({
    components: { CVPost, CVPost },
    setup() {

        const vacs = useVacancyStore()
        const authStores = useAuthStore()

        onMounted(() => {
            vacs.Vacancy()
        })
        return {
            auth: authStores,
            vacancy: vacs
        }
    },
    data() {
        return {
            showChange: false,
            searchQuery: '',
            changedVacancy: {
                id: 0,
                title: '',
                description: '',
                required_person: 0,
                is_active: true,
            },


        }
    },
    computed: {
        filteredVacancies() {
            const query = this.searchQuery.toLowerCase();
            return this.vacancy.getVacancyData.filter((vac) => {
                return vac.title.toLowerCase().includes(query) ||
                    vac.description.toLowerCase().includes(query)
            });
        }
    },

    methods: {
        fileHandle(e) {
            this.CV.photo = e.target.files[0];
        },


        show() {
            this.vacancy.showForm = !this.vacancy.showForm;
            this.vacancy.showVac = !this.vacancy.showVac;
        },

        showVacancy() {
            this.vacancy.showVac = !this.vacancy.showVac;
            this.showChange = !this.showChange;

            this.changedVacancy.id = 0;
            this.changedVacancy.title = '';
            this.changedVacancy.description = '';
            this.changedVacancy.required_person = 0;
        },

        async changeVacancy(Vacancy) {
            this.showChange = !this.showChange;
            this.vacancy.showVac = !this.vacancy.showVac;
            this.changedVacancy.id = Vacancy.id;
            this.changedVacancy.title = Vacancy.title;
            this.changedVacancy.description = Vacancy.description;
            this.changedVacancy.required_person = Vacancy.required_person;
            // console.log(this.changedVacancy)
        },

        modalShowSuccess() {
            if (this.vacancy.message === 'Updated') {
                return {
                    modal: 'modal fade show'
                }
            } else {
                return {
                    modal: 'modal fade'
                }
            }
        }
    }
})
</script>

<style scoped>
.size {
    width: 40%;
    margin: 0 auto;
}

.form-label {
    margin-top: 10px;
    position: relative;
}

.form-control {
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    box-sizing: border-box;
}

textarea.form-control {
    resize: vertical;
}

.floating-label {
    position: absolute;
    pointer-events: none;
    left: 8px;
    top: 15px;
    transition: 0.2s ease all;
}

.form-control:focus+.floating-label,
.form-control:not(:placeholder-shown)+.floating-label {
    top: 0;
    left: 0;
    font-size: 12px;
    color: #3498db;
}

.btn-outline-primary {
    color: #3498db;
    background-color: transparent;
    background-image: none;
    border-color: #3498db;
}

.btn-outline-primary:hover {
    color: #fff;
    background-color: #3498db;
    border-color: #3498db;
}

.mt-3 {
    margin-top: 15px;
}

form {
    padding: 15px;
    border: 1px solid #3498db;
    border-radius: 8px;
    background-color: #ecf0f1;
}

h2 {
    color: #3498db;
}

.text-danger {
    color: #e74c3c;
}

.bg-warning-subtle {
    background-color: #fff3cd;
}

.bg-danger-subtle {
    background-color: #f8d7da;
}

.bg-info-subtle {
    background-color: #d1ecf1;
}

.bg-dark-subtle {
    background-color: #343a40;
    color: #fff;
}

.card {
    background: #ffffff3f;
}

.card-footer {
    border-top: none;
}

.upd {
    border-radius: 5px;
    background: whitesmoke;
    box-shadow: 0 0 10px;
    padding: 2%;

}

.custom-btn {
    padding: 8px 16px;
    border: none;
    cursor: pointer;
    border-radius: 4px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.custom-btn.primary {
    background-color: #546e7ac7;
    color: #fff;
}

.custom-btn.primary:hover {
    background-color: #4b5b63;
}

.custom-btn.danger {
    background-color: #1b2329;
    color: #fff;
}

.custom-btn.danger:hover {
    background-color: #30444e;
}

.custom-btn.warning {
    background-color: #546e7a38;
    color: #fff;
}

.custom-btn.warning:hover {
    background-color: #3e5966;
}</style> 