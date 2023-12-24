<template>
    <div class="container text-center mt-5 outer">
        <h1 class="h1 my-3" v-if="dataCv.CVs.length === 0">Нет резюме!</h1>
        <div v-else>
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
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="download(null)">За весь период</button>
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="download('today')">За сегодня</button>
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="download('week')">За неделю</button>
                        <button class="btn btn-outline-dark border-0 container-fluid" @click="download('month')">За месяц</button>
                        <div class="dropdown-item">
                            <label for="startDate">От:</label>
                            <input type="date" id="startDate" class="form-control" v-model="startDate">
                        </div>
                        <div class="dropdown-item">
                            <label for="endDate">До:</label>
                            <input type="date" id="endDate" class="form-control" v-model="endDate">
                        </div>
                        <button class="btn btn-outline-dark border-0 container-fluid" style="--bs-btn-border-radius: none;" @click="download([startDate, endDate])">Скачать по периоду</button>
                    </div>
                </div>
            </div>



            <div class="row">
                <div class="col-md-4" v-if="short" v-for="cv in dataCv.CVs" :key="cv.id">
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
                                <img :src="getPhoto(cv.photo)" class="img-fluid" alt="Фото отправителя">
                            </div>
                            <div v-else>
                                <span>Нет фото</span>
                            </div>
                            <button class="btn btn-primary mt-2" data-toggle="modal" data-target="#detailsModal{{ cv.id }}"
                                @click="extend(cv); getLike(cv);">Подробнее</button>
                        </div>

                    </div>
                </div>
                <div class="col-md-12" v-else>
                    <div class="card mb-4 inner"
                        :class="{ 'card-status-viewed': selectedCv.is_viewed, 'card-status-accepted': selectedCv.is_accept, 'card-status-declined': selectedCv.is_declined }">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h3 class="card-title">{{ selectedCv.first_name }} {{ selectedCv.last_name }} {{
                                        selectedCv.middle_name }}</h3>

                                    <div><strong>Дата рождения:</strong> {{ selectedCv.was_born }}</div>

                                    <div><strong>Город:</strong> {{ selectedCv.where_from }}</div>

                                    <div v-if="selectedCv.about_me"><strong>О себе:</strong> {{ selectedCv.about_me }}</div>

                                    <div v-if="selectedCv.education"><strong>Образование:</strong> {{ selectedCv.education
                                    }}
                                    </div>

                                    <div v-if="selectedCv.where_to"><strong>Адресс проживания</strong> {{
                                        selectedCv.where_to }}</div>

                                    <div><strong>Желаемое место работы:</strong> {{ selectedCv.job_title.title }}</div>

                                    <div v-if="selectedCv.job_xp"><strong>Опыт работы:</strong> {{ selectedCv.job_xp }}
                                    </div>

                                    <div v-if="selectedCv.skills"><strong>Навыки:</strong> {{ selectedCv.skills }}</div>

                                    <div v-if="selectedCv.languages"><strong>Языки:</strong> {{ selectedCv.languages }}
                                    </div>

                                    <div><strong>Дата создания:</strong> {{ selectedCv.created_at }}</div>

                                    <div v-if="selectedCv.is_accept"><strong>Статус:</strong> Принято</div>
                                    <div v-if="selectedCv.is_declined"><strong>Статус:</strong> Отклонено</div>
                                    <div v-if="selectedCv.is_viewed"><strong>Статус:</strong> Просмотрено</div>
                                </div>
                                <div class="col-md-6 text-center">
                                    <div v-if="selectedCv.photo">
                                        <img :src="getPhoto(selectedCv.photo)" class="img-fluid" alt="Фото отправителя">
                                    </div>
                                    <div v-else>
                                        <span>Нет фото</span>
                                    </div>
                                </div>
                            </div>

                            <div class="col-md-12 mt-3">
                                <span class="text-info" v-if="isAdmin || isStaff">
                                    Сколько человек одобряет: {{ howMuch.data.like }}<br>
                                    Сколько человек не одобряет: {{ howMuch.data.dislike }}
                                </span>
                                <div v-else>
                                    <div>
                                        <p>Нельзя повторно отправить после первого нажатия. Если возникли проблемы с
                                            изначальным
                                            нажатием, возможно, кнопка была нажата ранее</p>
                                    </div>
                                    <div class="btn-group btn-group-sm mt-2">
                                        <button class="btn btn-outline-success " :disabled='slike || sdislike'
                                            @click="like(selectedCv.id)">Одобряю!</button>
                                        <button class="btn btn-outline-danger " :disabled='sdislike || slike'
                                            @click="dislike(selectedCv.id)">Не одобряю!</button> <br>
                                    </div>
                                </div>

                            </div>
                            <div class="col-md-12 mt-2" v-if="isAdmin || isStaff">
                                <div class="col-md-6 btn-group btn-group-sm">
                                    <button class="btn btn-danger mt-2" @click="deleteCv(selectedCv)">Удалить</button>
                                    <button class="btn btn-secondary mt-2" data-toggle="modal"
                                        @click="shorten">Коротко</button>
                                    <button class="btn btn-outline-success mt-2"
                                        @click="accept(selectedCv)">Принять</button>
                                    <button class="btn btn-outline-danger mt-2"
                                        @click="decline(selectedCv)">Отклонить</button>
                                </div>
                            </div>
                            <div class="col-md-12 mt-2" v-else-if="isMaster">
                                <div class="col-md-6 btn-group btn-group-sm">
                                    <button class="btn btn-secondary mt-2" data-toggle="modal"
                                        @click="shorten">Коротко</button>
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
import axios from 'axios';
import { authStore } from "@/store/store";
export default {
    setup() {
        const auth = authStore();

        return {
             isAdmin: auth.isAdmin, 
             isStaff: auth.isStaff, 
             isMaster: auth.isMaster 
            };
    },
    data() {
        return {
            dataCv: { CVs: [] },
            short: true,
            selectedCv: null,
            slike: false,
            sdislike: false,
            howMuch: { data: [] },
            startDate: null,
            endDate: null,
        }
    },

    async mounted() {
        await this.getCv()

    },
    methods: {
        async like(cvId) {
            try {
                await axios.post(`http://127.0.0.1:8000/cv_rate_post/${cvId}/true/`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert("Успешно (Повторное нажатие не вызовет никаких изменений)")
                this.slike = true;
                this.sdislike = true;
            } catch (error) {
                console.error(error)
                alert('Что-то пошло не так!')
            }
        },

        async dislike(cvId) {
            try {
                await axios.post(`http://127.0.0.1:8000/cv_rate_post/${cvId}/false/`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert("Успешно (Повторное нажатие не вызовет никаких изменений)")
                this.sdislike = true;
                this.slike = true;

            } catch (error) {
                console.error(error)
                alert('Что-то пошло не так!')
            }
        },

        async accept(cv) {
            try {
                await axios.put(`http://127.0.0.1:8000/cv/${cv.id}/`, { is_accept: true },
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert('Успешно принято')
                this.short = true;
            } catch (error) {
                console.error(error)
            }
        },

        async deleteCv(cv) {
            try {
                const response = await axios.delete(`http://127.0.0.1:8000/cv/${cv.id}/`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert('Успешно удалено')
                this.short = true;
                window.location.reload();
            } catch (error) {
                console.error(error)
            }
        },

        async decline(cv) {
            try {
                await axios.put(`http://127.0.0.1:8000/cv/${cv.id}/`, { is_declined: true },
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    })
                alert('Успешно отклонено!')
                this.short = true;
            } catch (error) {
                console.error(error)
            }
        },

        async getCv() {
            if (this.isAdmin || this.isStaff) {
                try {
                    const response = await axios.get('http://127.0.0.1:8000/all_cv_boss/',
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    // console.log(response.data)
                    this.dataCv.CVs = response.data;
                    console.log(this.dataCv);
                } catch (error) {
                    console.log(error);
                    alert('У вас нету прав или ошибка на стороне сервера!')
                    this.$router.push({ name: 'Home' })
                }
            } else if (this.isMaster) {
                try {
                    const response = await axios.get('http://127.0.0.1:8000/all_cv/',
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    // console.log(response.data)
                    this.dataCv.CVs = response.data;
                    // console.log(this.dataCv);
                } catch (error) {
                    console.log(error);
                    alert('У вас нету прав или ошибка на стороне сервера!')
                    this.$router.push({ name: 'Home' })
                }
            }

        },

        getPhoto(urlPhoto) {
            return `http://127.0.0.1:8000${urlPhoto}`
        },

        shorten() {
            this.short = !this.short
        },

        async extend(cv) {
            this.short = !this.short
            this.selectedCv = cv;
            // console.log(this.selectedCv)
            if (this.selectedCv.is_viewed === false) {
                try {
                    await axios.put(`http://127.0.0.1:8000/cv/${cv.id}`, cv,
                        {
                            headers:
                            {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                } catch (error) {
                    console.error(error);
                }

            }

        },

        async getLike(cv) {
            if (this.isAdmin || this.isStaff) {
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/cv_rate_get/${cv.id}/`,
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    console.log(response.data)
                    this.howMuch.data = response.data;
                } catch (error) {
                    console.error(error);
                }
            } else if (this.isMaster) {
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/cv_rate_post/${this.selectedCv.id}/' '`,
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    if (response.status == 202) {
                        this.slike = true;
                        this.sdislike = true;
                    } else if (response.status == 204) {
                        this.slike = false;
                        this.sdislike = false;
                    }
                } catch (error) {
                    console.error(error);
                }
            }


        },

        async download(period) {
            // console.log(period);
            let url = '';
            let fileName = '';
            try {


                if (period === 'today') {
                    url = 'http://127.0.0.1:8000/download_xlsx/period/today';
                    fileName = 'Резюме за сегодня.xlsx';
                } else if (period === 'week') {
                    url = 'http://127.0.0.1:8000/download_xlsx/period/week';
                    fileName = 'Резюме за неделю.xlsx';
                } else if (period === 'month') {
                    url = 'http://127.0.0.1:8000/download_xlsx/period/month';
                    fileName = 'Резюме за месяц.xlsx';
                } else if (period === null) {
                    url = 'http://127.0.0.1:8000/download_xlsx/period/allTime';
                    fileName = 'Резюме за все время.xlsx';
                } else if (Array.isArray(period) && period.length === 2) {
                    const [start, end] = period;

                    if (start && end) {
                        url = `http://127.0.0.1:8000/download_xlsx/custom?startDate=${start}&endDate=${end}`;
                        fileName = `Резюме за ${start} по ${end}.xlsx`;
                    } else {
                        console.error('Введите обе даты');
                        return;
                    }
                }


                const response = await axios.get(url, {
                responseType: 'arraybuffer',
                headers: {
                    'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'Content-Disposition': `attachment; filename=${encodeURIComponent(fileName)}`,
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
            // console.log(response.data)
            const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = fileName;
            link.click();
        } catch(error) {
            console.error(error);
            // console.log(url)
        }
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