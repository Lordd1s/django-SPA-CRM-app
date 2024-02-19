<template>
    <div class="size mt-4">
        <div class="card mx-auto my-3 p-3">
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
                        <option :value="job.title" v-for="job in vacancy.getVacancyData" :key="job.id"> Должность {{
                            job.title }}
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
</template>

<script>
import { useVacancyStore } from '@/store/VacancyStore';
import axios from 'axios';
export default {
    setup() {
        const vacs = useVacancyStore()
        return {
            vacancy: vacs
        }
    },

    data() {
        return {
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
        }
    },

    methods: {
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
                console.error(error);
                alert('Резюме с такими данными существует!')

            }
        },
        show() {
            this.vacancy.showForm = !this.vacancy.showForm;
            this.vacancy.showVac = !this.vacancy.showVac;
        },
        fileHandle(e) {
            this.CV.photo = e.target.files[0];
        },
    },


}
</script>

<style scoped></style>