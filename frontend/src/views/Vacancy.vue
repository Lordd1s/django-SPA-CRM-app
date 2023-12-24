<template>
    <div class="text-center my-3" v-if="vacancy.data == ''">
        <span class="h1">Нет доступных вакансии</span>
    </div>

    <div class="size mt-4">
        <div class="card mx-auto my-3 p-3" v-if="showForm">
            <button class="btn btn-secondary mb-3" @click="show">Назад к вакансиям</button>
            <form @submit.prevent="postCV">
                <h2 class="h2">Откликнуться</h2>
                <p class="text-danger h5">* <span class="text-dark">Обязательные поля!</span></p>

                <div class="mb-3">
                    <label for="name" class="form-label">* Имя</label>
                    <input type="text" class="form-control" v-model="CV.name" id="name">
                </div>

                <div class="mb-3">
                    <label for="lastName" class="form-label">* Фамилия</label>
                    <input type="text" class="form-control" v-model="CV.lastName" id="lastName">
                </div>

                <div class="mb-3">
                    <label for="middleName" class="form-label">Отчество</label>
                    <input type="text" class="form-control" v-model="CV.middleName" id="middleName">
                </div>

                <div class="mb-3">
                    <label for="wasBorn" class="form-label">* Дата рождения</label>
                    <input type="date" class="form-control" v-model="CV.wasBorn" id="wasBorn">
                </div>

                <div class="mb-3">
                    <label for="phoneNumber" class="form-label">* Номер телефона</label>
                    <input type="tel" class="form-control" v-model="CV.phone_number" id="phoneNumber">
                </div>

                <div class="mb-3">
                    <label for="photo" class="form-label">Фото</label>
                    <input type="file" class="form-control" @change="fileHandle" id="photo">
                </div>

                <div class="mb-3">
                    <label for="whereFrom" class="form-label">* Место рождения</label>
                    <input type="text" class="form-control" v-model="CV.whereFrom" id="whereFrom">
                </div>

                <div class="mb-3">
                    <label for="whereTo" class="form-label">Место жительства</label>
                    <input type="text" class="form-control" v-model="CV.whereTo" id="whereTo">
                </div>

                <div class="mb-3">
                    <label for="education" class="form-label">Образование</label>
                    <input type="text" class="form-control" v-model="CV.education" id="education">
                </div>

                <div class="mb-3">
                    <label for="jobXp" class="form-label">Опыт работы</label>
                    <input type="text" class="form-control" v-model="CV.jobXp" id="jobXp">
                </div>

                <div class="mb-3">
                    <label for="jobTitle" class="form-label">* На должность</label>
                    <select class="form-select" v-model="CV.jobTitle" id="jobTitle">
                        <option :value="job.title" v-for="job in vacancy.data" :key="job.id"> Должность {{ job.title }}
                        </option>
                    </select>
                </div>

                <div class="mb-3">
                    <label for="skills" class="form-label">Навыки</label>
                    <input type="text" class="form-control" v-model="CV.skills" id="skills">
                </div>

                <div class="mb-3">
                    <label for="languages" class="form-label">Языки</label>
                    <input type="text" class="form-control" v-model="CV.languages" id="languages">
                </div>

                <div class="mb-3">
                    <label for="aboutMe" class="form-label">О себе</label>
                    <textarea type="text" class="form-control" v-model="CV.aboutMe" id="aboutMe"></textarea>
                </div>

                <button class="btn btn-primary mt-3 form-control">Отправить</button>
            </form>
            <button class="btn btn-secondary mt-3" @click="show">Назад к вакансиям</button>
        </div>
    </div>


    <div v-if="getagain" class="size text-center my-3">
        <span class="h5">Не загружается данные? Нажмите </span>
        <button class="btn btn-outline-dark btn-sm" @click="getAgain">Здесь</button>
    </div>

    <div class="form-floating size" v-if="showVac">
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
            <div class="card-footer d-flex justify-content-between" style="background-color: #27343c; color: #fff;">
                <div>
                    <p class="mb-1"><strong>Требуемый персонал:</strong> {{ vac.required_person }}</p>
                    <span><strong>Выложено:</strong> {{ vac.date_created }}</span>
                </div>
                <div class="custom-buttons">
                    <button class="btn custom-btn primary disabled" v-if="isAdmin || isStaff || isMaster"
                        >Откликнуться</button>
                    <button class="btn custom-btn danger" v-if="isAdmin || isStaff"
                        @click="deleteVacancy(vac)">Удалить</button>
                    <button class="btn custom-btn warning" v-if="isAdmin || isStaff"
                        @click="changeVacancy(vac)">Редактировать</button>
                    <button class="btn custom-btn primary" v-if="username === null" @click="show">Откликнуться</button>
                </div>
            </div>
        </div>
    </div>

    <div class="container mt-4" v-else>
        <div class="card mx-auto my-3 p-3" v-if="showVac" v-for="vac in vacancy.data" :key="vac.id">
            <h3 class="h3 card-header" style="background-color: #27343c; color: #fff;">{{ vac.title }}</h3>
            <div class="card-body" style="background-color: #546e7a; color: #fff;">
                <p v-if="vac.is_active" class="mb-3"><strong>Статус:</strong> Активно</p>
                <p v-else class="mb-3"><strong>Статус:</strong> Не активно</p>
                <p class="mb-3"><strong>Описание:</strong> {{ vac.description }}</p>
            </div>
            <div class="card-footer d-flex justify-content-between" style="background-color: #27343c; color: #fff;">
                <div>
                    <p class="mb-1"><strong>Требуемый персонал:</strong> {{ vac.required_person }}</p>
                    <span><strong>Выложено:</strong> {{ vac.date_created }}</span>
                </div>
                <div class="custom-buttons">
                    <button class="btn custom-btn primary disabled" v-if="isAdmin || isStaff || isMaster"
                        @click="show">Откликнуться</button>
                    <button class="btn custom-btn danger" v-if="isAdmin || isStaff"
                        @click="deleteVacancy(vac)">Удалить</button>
                    <button class="btn custom-btn warning" v-if="isAdmin || isStaff"
                        @click="changeVacancy(vac)">Редактировать</button>
                    <button class="btn custom-btn primary" v-else @click="show">Откликнуться</button>
                </div>
            </div>
        </div>
    </div>
    <div class="size upd mt-5" v-if="showChange">
        <form @submit.prevent="updVac">
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
        <button class="btn btn-outline-secondary form-control mt-3" @click="showVacancy">Вернуться к вакансиям</button>
    </div>
</template>

<script>
import axios from 'axios';
import { defineComponent } from 'vue';
import { authStore } from '@/store/store';

export default defineComponent({
    setup() {
        const authStores = authStore()
        return { 
            isAdmin: authStores.isAdmin, 
            isStaff: authStores.isStaff, 
            isMaster: authStores.isMaster, 
            username: authStores.username, 
        }
    },
    data() {
        return {
            vacancy: { data: [] },
            showForm: false,
            showChange: false,
            showVac: true,
            getagain: true,
            searchQuery: '',
            CV: {
                name: '',
                lastName: '',
                middleName: '',
                wasBorn: '',
                phone_number: '',
                photo: null,
                whereFrom: '',
                whereTo: '',
                education: '',
                jobXp: '',
                jobTitle: '',
                skills: '',
                languages: '',
                aboutMe: '',
            },
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
            return this.vacancy.data.filter((vac) => {
                return vac.title.toLowerCase().includes(query) ||
                    vac.description.toLowerCase().includes(query)
            });
        }
    },
    async mounted() {
        await this.Vacancy();
    },
    methods: {
        fileHandle(e) {
            this.CV.photo = e.target.files[0];
        },

        async Vacancy() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/vacancy/");
                // console.log(response);
                this.vacancy = { ...response }
                // console.log(this.vacancy)
            } catch (error) {
                console.error(error);

            }

        },

        async getAgain() {
            await this.Vacancy()
            // window.location.reload()
        },


        show() {
            this.showForm = !this.showForm;
            this.showVac = !this.showVac;
            this.getagain = !this.getagain;
        },
        showVacancy() {
            this.showVac = !this.showVac;
            this.showChange = !this.showChange;
            this.getagain = !this.getagain;

            this.changedVacancy.id = 0;
            this.changedVacancy.title = '';
            this.changedVacancy.description = '';
            this.changedVacancy.required_person = 0;
        },

        async changeVacancy(Vacancy) {
            this.showChange = !this.showChange;
            this.showVac = !this.showVac;
            this.changedVacancy.id = Vacancy.id;
            this.changedVacancy.title = Vacancy.title;
            this.changedVacancy.description = Vacancy.description;
            this.changedVacancy.required_person = Vacancy.required_person;

        },

        async deleteVacancy(vacancy) {
            // console.log(vacancy)
            try {
                await axios.delete(`http://127.0.0.1:8000/cud_vacancy/${vacancy.id}/`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert('Успешно удалено!')
                this.vacancy.data = this.vacancy.data.filter(item => item.id !== vacancy.id);
            } catch (error) {
                console.error(error);
                alert('Не удалось удалить вакансию!')
            }
        },

        async updVac() {
            try {
                await axios.put(`http://127.0.0.1:8000/cud_vacancy/${this.changedVacancy.id}/`, this.changedVacancy,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert('Успешно обновлен!')
                this.$router.push({ name: 'Vacancy' })
                this.showVac = !this.showVac;
                this.showChange = !this.showChange
            } catch (error) {
                console.error(error)
            }
        },

        async postCV() {
            try {
                await axios.post("http://127.0.0.1:8000/cv/' '/", this.CV, {
                    headers: {
                        'Content-Type': 'multipart/form-data; charset=utf-8',
                    }
                });
                // console.log(this.CV)
                // console.log(request);
                alert('Ваше резюме успешно отправлено!');
                this.showForm = false;
                this.showVac = true;
                this.$router.push({ name: 'Vacancy' });
                this.CV = {
                    name: '',
                    lastName: '',
                    middleName: '',
                    wasBorn: '',
                    phone_number: '',
                    photo: null,
                    whereFrom: '',
                    whereTo: '',
                    education: '',
                    jobXp: '',
                    jobTitle: '',
                    skills: '',
                    languages: '',
                    aboutMe: '',
                }
            } catch (error) {
                if (error.response.status === 403) {
                    alert('Резюме с такими данными существует!')
                }
                console.error(error);
                alert('Резюме с такими данными существует!')

            }
        },


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
}
</style> 