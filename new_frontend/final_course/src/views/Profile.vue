<template>
    <div v-if="profil.getProfile.length === 1">
        <div class="profile-container bg-light" v-if="showForm === false">
            <div class="profile-header bg-dark">
                <img :src="profil.getAvatar" alt="Аватар" class="profile-image">
                <div class="profile-name"></div>
            </div>
            <div class="profile-details">
                <!-- Имя -->
                <div class="detail-item" v-if="profil.getProfile.user.first_name">
                    <span class="detail-label">Имя:</span>
                    <span class="detail-value">{{ profil.getProfile.user.first_name }}</span>
                </div>
                <div class="detail-item" v-else>
                    <span class="detail-label">Имя:</span>
                    <span class="detail-value">Не указано</span>
                </div>
                <!-- Фамилия -->
                <div class="detail-item" v-if="profil.getProfile.user.last_name">
                    <span class="detail-label">Фамилия:</span>
                    <span class="detail-value">{{ profil.getProfile.user.last_name }}</span>
                </div>
                <div class="detail-item" v-else>
                    <span class="detail-label">Фамилия:</span>
                    <span class="detail-value">Не указано</span>
                </div>
                <!-- Почта -->
                <div class="detail-item">
                    <span class="detail-label">Почта:</span>
                    <span class="detail-value">{{ auth.getUser.email }}</span>
                </div>
                <!-- Телефон -->
                <div class="detail-item" v-if="profil.getProfile.phone_number">
                    <span class="detail-label">Телефон:</span>
                    <span class="detail-value">{{ profil.getProfile.phone_number }}</span>
                </div>
                <div class="detail-item" v-else>
                    <span class="detail-label">Телефон:</span>
                    <span class="detail-value">Не указано</span>
                </div>
                <!-- Юзернейм -->
                <div class="detail-item">
                    <span class="detail-label">Имя пользователя:</span>
                    <span class="detail-value">{{ auth.getUser.username }}</span>
                </div>
                <!-- Дата рождения -->
                <div class="detail-item" v-if="profil.getProfile.was_born">
                    <span class="detail-label">Дата рождения:</span>
                    <span class="detail-value">{{ profil.getProfile.was_born }}</span>
                </div>
                <div class="detail-item" v-else="profil.getProfile.was_born">
                    <span class="detail-label">Дата рождения:</span>
                    <span class="detail-value">Не указано</span>
                </div>

            </div>

            <div class="profile-actions">
                <button class="edit-profile-btn" @click="show">Редактировать профиль</button>
            </div>
        </div>
        <div v-if="showForm">
            <form @submit.prevent="send.sendUpdProfile(updForm)">
                <div class="form-container">
                    <div :class="modalShowLoading" id="exampleModalCenter" tabindex="-1" aria-labelledby="exampleModalCenterTitle"
            aria-modal="true" role="dialog" style="display: block;" v-if="profil.loading">
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
                aria-modal="true" role="dialog" style="display: block;" v-if="profil.error">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3 class="modal-title">Ошибка!</h3>
                        </div>
                        <div class="modal-title">
                            <p class="modal-title">Заполните все поле!</p>
                        </div>

                    </div>
                </div>
            </div>
                    <button type="button" class="btn btn-outline-info mb-3 w-100" @click="show">Назад</button>
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
                        <label for="photo">Аватар</label>
                        <input type="file" id="photo" name="avatar" @change="fileHandle">
                    </div>

                    <button>Отправить</button>
                </div>
            </form>
        </div>

    </div>
    <div v-else class="m-5 text-light mx-auto w-100 h1 text-center">
        Загрузка данных...
        <div class="spinner-border spinner-border-sm" role="status"></div>
    </div>
</template>

<script>
import { useAuthStore } from '@/store/AuthStore';
import { useProfileStore } from '@/store/ProfileStore';
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
    setup() {
        const authStores = useAuthStore()
        const prof = useProfileStore()
        onMounted(() => {
            prof.getProfileFromBack()
            useProfileStore().restoreProfile
        })
        return {
            auth: authStores,
            email: authStores.email,
            username: authStores.username,
            userId: authStores.userId,
            profil: prof,
            send: prof,
        }
    },

    data() {
        return {
            updForm: {
                first_name: '',
                last_name: '',
                phone_number: '',
                was_born: '',
                avatar: null,

            },
            showForm: false,
        }
    },

    methods: {
        show() {
            this.showForm = !this.showForm;
        },
        fileHandle(e) {
            this.updForm.avatar = e.target.files[0];
        },

        modalShowError() {
            console.log(this.profile.error)
            if (this.profil.error) {
                console.log(this.profile.error)
                return { modal: 'modal fade show' }
            } else {
                console.log(this.profile.error)
                return { modal: 'modal fade' }
            }
        },
        modalShowLoading() {
            if (this.profil.loading) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },

    }
})
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