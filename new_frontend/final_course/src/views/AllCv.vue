<template>
    <div class="container text-center mt-5 outer">
        <h1 class="h1 my-3" v-if="cvStore.getCVs.length === 0">Нет резюме!</h1>
        <div v-else>
            <section>
                <div :class="modalShowLoading" id="exampleModalCenter" tabindex="-1"
                    aria-labelledby="exampleModalCenterTitle" aria-modal="true" role="dialog" style="display: block;"
                    v-if="cvStore.loading">
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
                    aria-modal="true" role="dialog" style="display: block;" v-if="cvStore.error">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h3 class="modal-title">Ошибка!</h3>
                            </div>
                            <div class="modal-title">
                                <p class="modal-title">{{ cvStore.error }}</p>
                            </div>

                        </div>
                    </div>
                </div>
            </section>
            <div class="btn-group">
                <span class="card-status-viewed p-1 border-end-0">"Просмотрено"</span>
                <span class="card-status-accepted p-1 border-start-0 border-end-0">"Принято"</span>
                <span class="card-status-declined p-1 border-start-0">"Отклонено"</span>
            </div>


            <h1 class="h1 my-3">Все резюме!</h1>
            <div class="btn-group mb-3">

                <div>
                    <button class="btn btn-dark" data-bs-toggle="dropdown">Скачать весь резюме в .xlsx <i
                            class="bi bi-caret-down"></i></button>
                    <div class="dropdown-menu">
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="cvStore.download(null)">За
                            весь период</button>
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="cvStore.download('today')">За
                            сегодня</button>
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="cvStore.download('week')">За
                            неделю</button>
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="cvStore.download('month')">За
                            месяц</button>
                        <div class="dropdown-item">
                            <label for="startDate">От:</label>
                            <input type="date" id="startDate" class="form-control" v-model="startDate">
                        </div>
                        <div class="dropdown-item">
                            <label for="endDate">До:</label>
                            <input type="date" id="endDate" class="form-control" v-model="endDate">
                        </div>
                        <button class="btn btn-outline-dark border-0 container-fluid" style="--bs-btn-border-radius: none;"
                            @click="cvStore.download([startDate, endDate])">Скачать по периоду</button>
                    </div>
                </div>
            </div>



            <div class="row">
                <div class="col-md-4" v-if="cvStore.short" v-for="cv in cvStore.getCVs" :key="cv.id">
                    <div class="card mb-4 inner">
                        <div class="card-body"
                            :class="{ 'card-status-viewed': cv.is_viewed, 'card-status-accepted': cv.is_accept, 'card-status-declined': cv.is_declined }">
                            <h5 class="card-title">Имя: {{ cv.first_name }}</h5>
                            <p class="card-text">Город: {{ cv.where_from }}</p>
                            <div class="progress my-3" role="progressbar" aria-label="Danger" aria-valuenow="cv.rating"
                                aria-valuemin="0" aria-valuemax="25" v-if="cv.rating > 0 && cv.rating <= 25">
                                <div class="progress-bar-striped progress-bar-animated bg-danger" style="width: 25%">Рейтинг
                                    {{ cv.rating }} %</div>
                            </div>
                            <div class="progress my-3" role="progressbar" aria-label="Warning" aria-valuenow="cv.rating"
                                aria-valuemin="0" aria-valuemax="50" v-else-if="cv.rating > 25 && cv.rating <= 50">
                                <div class="progress-bar-striped progress-bar-animated bg-warning" style="width: 50%">
                                    {{ cv.rating }} %</div>
                            </div>
                            <div class="progress my-3" role="progressbar" aria-label="Info" aria-valuenow="cv.rating"
                                aria-valuemin="0" aria-valuemax="75" v-else-if="cv.rating > 50 && cv.rating <= 99">
                                <div class="progress-bar-striped progress-bar-animated bg-info" style="width: 75%">Рейтинг
                                    {{ cv.rating }} %</div>
                            </div>
                            <div class="progress my-3" role="progressbar" aria-label="Success" aria-valuenow="cv.rating"
                                aria-valuemin="0" aria-valuemax="100" v-if="cv.rating == 100">
                                <div class="progress-bar-striped progress-bar-animated bg-success" style="width: 100%">
                                    Рейтинг {{ cv.rating }} %</div>
                            </div>
                            <div v-if="cv.photo">
                                <img :src="Photo(cv.photo)" class="img-fluid" alt="Фото отправителя">
                            </div>
                            <div v-else>
                                <span>Нет фото</span>
                            </div>
                            <button class="btn btn-primary mt-2" data-toggle="modal" data-target="#detailsModal{{ cv.id }}"
                                @click="cvStore.extend(cv); cvStore.getLike(cv);">Подробнее</button>
                        </div>

                    </div>
                </div>
                <div class="col-md-12" v-else>
                    <div class="card mb-4 inner"
                        :class="{ 'card-status-viewed': cvStore.getSelected.is_viewed, 'card-status-accepted': cvStore.getSelected.is_accept, 'card-status-declined': cvStore.getSelected.is_declined }">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h3 class="card-title">{{ cvStore.getSelected.first_name }} {{
                                        cvStore.getSelected.last_name }} {{
        cvStore.getSelected.middle_name }}</h3>

                                    <div><strong>Дата рождения:</strong> {{ cvStore.getSelected.was_born }}</div>

                                    <div><strong>Город:</strong> {{ cvStore.getSelected.where_from }}</div>

                                    <div v-if="cvStore.getSelected.about_me"><strong>О себе:</strong> {{
                                        cvStore.getSelected.about_me }}</div>

                                    <div v-if="cvStore.getSelected.education"><strong>Образование:</strong> {{
                                        cvStore.getSelected.education
                                    }}
                                    </div>

                                    <div v-if="cvStore.getSelected.where_to"><strong>Адресс проживания</strong> {{
                                        cvStore.getSelected.where_to }}</div>

                                    <div><strong>Желаемое место работы:</strong> {{ cvStore.getSelected.job_title.title }}
                                    </div>

                                    <div v-if="cvStore.getSelected.job_xp"><strong>Опыт работы:</strong> {{
                                        cvStore.getSelected.job_xp }}
                                    </div>

                                    <div v-if="cvStore.getSelected.skills"><strong>Навыки:</strong> {{
                                        cvStore.getSelected.skills }}</div>

                                    <div v-if="cvStore.getSelected.languages"><strong>Языки:</strong> {{
                                        cvStore.getSelected.languages }}
                                    </div>

                                    <div><strong>Дата создания:</strong> {{ cvStore.getSelected.created_at }}</div>

                                    <div v-if="cvStore.getSelected.is_accept"><strong>Статус:</strong> Принято</div>
                                    <div v-if="cvStore.getSelected.is_declined"><strong>Статус:</strong> Отклонено</div>
                                    <div v-if="cvStore.getSelected.is_viewed"><strong>Статус:</strong> Просмотрено</div>
                                </div>
                                <div class="col-md-6 text-center">
                                    <div v-if="cvStore.getSelected.photo">
                                        <img :src="Photo(cvStore.getSelected.photo)" class="img-fluid" alt="Фото отправителя">
                                    </div>
                                    <div v-else>
                                        <span>Нет фото</span>
                                    </div>
                                </div>
                            </div>

                            <div class="col-md-12 mt-3">
                                <span class="text-info" v-if="auth.getUser.isAdmin || auth.getUser.isStaff">
                                    Сколько человек одобряет: {{ cvStore.getHowMuch.like }}<br>
                                    Сколько человек не одобряет: {{ cvStore.getHowMuch.dislike }}
                                </span>
                                <div v-else>
                                    <div>
                                        <p>Нельзя повторно отправить после первого нажатия. Если возникли проблемы с
                                            изначальным
                                            нажатием, возможно, кнопка была нажата ранее</p>
                                    </div>
                                    <div class="btn-group btn-group-sm mt-2">
                                        <button class="btn btn-outline-success " :disabled='cvStore.slike || cvStore.sdislike'
                                            @click="cvStore.like(cvStore.getSelected.id)">Одобряю!</button>
                                        <button class="btn btn-outline-danger " :disabled='cvStore.sdislike || cvStore.slike'
                                            @click="cvStore.dislike(cvStore.getSelected.id)">Не одобряю!</button> <br>
                                    </div>
                                </div>

                            </div>
                            <div class="col-md-12 mt-2" v-if="auth.getUser.isAdmin || auth.getUser.isStaff">
                                <div class="col-md-6 btn-group btn-group-sm">
                                    <button class="btn btn-danger mt-2"
                                        @click="cvStore.deleteCv(cvStore.getSelected)">Удалить</button>
                                    <button class="btn btn-secondary mt-2" data-toggle="modal"
                                        @click="cvStore.shorten()">Коротко</button>
                                    <button class="btn btn-outline-success mt-2"
                                        @click="cvStore.accept(cvStore.getSelected)">Принять</button>
                                    <button class="btn btn-outline-danger mt-2"
                                        @click="cvStore.decline(cvStore.getSelected)">Отклонить</button>
                                </div>
                            </div>
                            <div class="col-md-12 mt-2" v-else-if="auth.getUser.isMaster">
                                <div class="col-md-6 btn-group btn-group-sm">
                                    <button class="btn btn-secondary mt-2" data-toggle="modal"
                                        @click="cvStore.shorten()">Коротко</button>
                                </div>
                            </div>


                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from "@/store/AuthStore";
import { useCvStore } from "@/store/CVStore";
import { onMounted } from "vue";
export default {
    setup() {
        const auth = useAuthStore();
        const cvStore = useCvStore();

        onMounted(() => {
            cvStore.getCv()
        })

        return {
            auth: auth,
            cvStore: cvStore
        };
    },
    data() {
        return {
            startDate: null,
            endDate: null,
        }
    },

    methods: {
        modalShowError() {
            if (this.cvStore.error) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },
        modalShowLoading() {
            if (this.cvStore.error) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },
        Photo(photo) {
            return this.cvStore.getPhoto(photo)
        }
    },

}
</script>

<style scoped>
.outer {
    background-color: #f8f9fa5d;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 2% auto;
}

.h1 {
    color: #007bff;
    font-size: 28px;
}

.inner {
    margin-bottom: 20px;
    transition: transform 0.3s ease-in-out;
}

.inner:hover {
    transform: scale(1.05);
}

.card {
    border: none;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.fio span {
    font-weight: bold;
    color: #343a40;
}

.address span {
    color: #6c757d;
}

.photo {
    margin-top: 10px;
}

.btn-primary {
    background-color: #28a745;
    border-color: #28a745;
    transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out;
}

.btn-primary:hover {
    background-color: #218838;
    border-color: #218838;
}

.card-status-viewed {
    border: 2px solid #17a2b8;
    /* Цвет для просмотренных */
    background-color: #edf8fb;
    /* Фон для просмотренных */
}

.card-status-accepted {
    border: 2px solid #28a745;
    /* Цвет для принятых */
    background-color: #d4edda;
    /* Фон для принятых */
}

.card-status-declined {
    border: 2px solid #dc3545;
    /* Цвет для отклоненных */
    background-color: #f8d7da;
    /* Фон для отклоненных */
}

/* Дополнительные стили для карточки на всю ширину */
.card.mb-4.inner {
    width: 100%;
    box-sizing: border-box;
}

/* Дополнительные стили для изображения */
.img-fluid {
    max-width: 100%;
    height: auto;
}
</style>