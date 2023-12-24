<template>
    <div class="m-5 text-light mx-auto w-100 h1" v-if="profil === null">
       Загрузка данных...
        <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">   Loading...</span>
        </div>
    </div>
    <div v-else>
        <div class="profile-container bg-light" v-if="showForm === false">
            <div class="profile-header bg-dark">
                <img :src="getAvatar()" alt="Аватар" class="profile-image">
                <div class="profile-name"></div>
            </div>
            <div class="profile-details">
                <!-- Имя -->
                <div class="detail-item" v-if="profil.user.first_name">
                    <span class="detail-label">Имя:</span>
                    <span class="detail-value">{{ profil.user.first_name }}</span>
                </div>
                <div class="detail-item" v-else>
                    <span class="detail-label">Имя:</span>
                    <span class="detail-value">Не указано</span>
                </div>
                <!-- Фамилия -->
                <div class="detail-item" v-if="profil.user.last_name">
                    <span class="detail-label">Фамилия:</span>
                    <span class="detail-value">{{ profil.user.last_name }}</span>
                </div>
                <div class="detail-item" v-else>
                    <span class="detail-label">Фамилия:</span>
                    <span class="detail-value">Не указано</span>
                </div>
                <!-- Почта -->
                <div class="detail-item">
                    <span class="detail-label">Почта:</span>
                    <span class="detail-value">{{ profil.user.email }}</span>
                </div>
                <!-- Телефон -->
                <div class="detail-item" v-if="profil.phone_number">
                    <span class="detail-label">Телефон:</span>
                    <span class="detail-value">{{ profil.phone_number }}</span>
                </div>
                <div class="detail-item" v-else>
                    <span class="detail-label">Телефон:</span>
                    <span class="detail-value">Не указано</span>
                </div>
                <!-- Юзернейм -->
                <div class="detail-item">
                    <span class="detail-label">Имя пользователя:</span>
                    <span class="detail-value">{{ profil.user.username }}</span>
                </div>
                <!-- Дата рождения -->
                <div class="detail-item" v-if="profil.was_born">
                    <span class="detail-label">Дата рождения:</span>
                    <span class="detail-value">{{ profil.was_born }}</span>
                </div>
                <div class="detail-item" v-else="profil.was_born">
                    <span class="detail-label">Дата рождения:</span>
                    <span class="detail-value">Не указано</span>
                </div>

            </div>

            <div class="profile-actions">
                <button class="edit-profile-btn" @click="show">Редактировать профиль</button>
            </div>
        </div>
        <div v-if="showForm">
            <form @submit.prevent="sendUpdProfile">
                <div class="form-container">
                    <h2 class="h2 text-center">Изменение данных</h2>

                    <div class="form-group">
                        <label for="firstName">Имя:</label>
                        <input type="text" id="firstName" name="firstName" placeholder="Введите ваше имя" 
                            v-model="updForm.first_name">
                    </div>

                    <div class="form-group">
                        <label for="lastName">Фамилия:</label>
                        <input type="text" id="lastName" name="lastName" placeholder="Введите вашу фамилию" 
                            v-model="updForm.last_name">
                    </div>

                    <div class="form-group">
                        <label for="dob">Дата рождения:</label>
                        <input type="date" id="dob" name="dob" v-model="updForm.was_born">
                    </div>

                    <div class="form-group">
                        <label for="phoneNumber">Номер телефона:</label>
                        <input type="tel" id="phoneNumber" name="phoneNumber" placeholder="Введите номер телефона"
                            v-model="updForm.phone_number">
                    </div>

                    <div class="form-group">
                        <label for="photo">Номер телефона:</label>
                        <input type="file" id="photo" name="phoneNumber"
                            @change="fileHandle">
                    </div>

                    <button>Отправить</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { authStore, profile } from '@/store/store';
import axios from "axios";
import { onMounted } from 'vue';

export default {
    setup() {
        const authStores = authStore()
        const prof = profile()
        return { 
            userId: authStores.userId, 
            profil: prof.prof 
        }
    },

    data() {
        return {
            showForm: false,
            updForm: {
                first_name: '',
                last_name: '',
                phone_number: '',
                was_born: '',
                avatar: null
            }
        }
    },

    async mounted() {
        await this.userGet()
    },

    methods: {
        async userGet() {
            // console.log(this.userId)
            if (this.profil === null) {
                try {
                    const res = await axios.get(`http://127.0.0.1:8000/profile/?userId=${this.userId}`,
                        {
                            headers: {
                                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                            }
                        })
                    // console.log(res.data)
                    onMounted(() => {
                        profile().addData(res.data)
                    });
                    // this.profil = res.data
                    console.log(this.profil)
                    console.log(this.profil.user)
                } catch (error) {
                    alert(error)
                    console.error(error)
                }
            }

        },

        getAvatar() {
            // console.log(`http://127.0.0.1:8000${this.profile.avatar}`)
            return `http://127.0.0.1:8000${this.profil.avatar}`
        },

        show() {
            this.showForm = !this.showForm
        },

        async sendUpdProfile() {
            try {
                const request = await axios.patch(`http://127.0.0.1:8000/profile/?userId=${this.userId}`, this.updForm,
                    {
                        headers: {
                            "Content-Type": 'multipart/form-data; charset=utf-8',
                            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                        }
                    }
                )
                if (request.status == 201) {
                    alert('Успешно отравлено')
                    this.profil.user.first_name = this.updForm.first_name
                    this.profil.user.last_name = this.updForm.last_name
                    this.profil.phone_number = this.updForm.phone_number
                    this.profil.was_born = this.updForm.was_born
                    this.showForm = !this.showForm
                } else if (request.status == 400) {
                    alert('Заполните хоть одно поле!')
                }
            } catch (error) {
                alert(error)
                console.log(error)
            }
        },

        fileHandle(e) {
            this.updForm.avatar = e.target.files[0];
        }
    }
}
</script>

<style scoped>
.profile-container {
    max-width: 600px;
    margin: 50px auto;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 0 5px;
}

.profile-header {
    color: #fff;
    text-align: center;
    padding: 20px;
}

.profile-image {
    border-radius: 50%;
    width: 120px;
    height: 120px;
    object-fit: cover;
    border: 4px solid #fff;
}

.profile-name {
    font-size: 24px;
    margin-top: 10px;
}

.profile-details {
    padding: 20px;
}

.detail-item {
    margin-bottom: 15px;
}

.detail-label {
    font-weight: bold;
    display: inline-block;
    width: 120px;
    color: #555;
}

.detail-value {
    display: inline-block;
    color: #333;
}

.profile-actions {
    text-align: center;
    padding: 20px;
}

.edit-profile-btn {
    background-color: #27ae60;
    color: #fff;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.edit-profile-btn:hover {
    background-color: #218c54;
}

/* Form */

.form-container {
    max-width: 400px;
    margin: 50px auto;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    padding: 20px;
    box-sizing: border-box;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
}

input {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 4px;
    margin-bottom: 12px;
    font-size: 16px;
}

button {
    background-color: #3498db;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #218c54;
}

/* Добавленные цвета */
label,
button {
    padding: 1%;
    background-color: #c1e648;
    color: #864c86;
}
</style>