<template>
    <div class="my-5 p-3 bg-light-subtle rounded w-25 mx-auto">
        <div :class="modalShowLoading" id="exampleModalCenter" tabindex="-1" aria-labelledby="exampleModalCenterTitle"
            aria-modal="true" role="dialog" style="display: block;" v-if="auth.loading">
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
            aria-modal="true" role="dialog" style="display: block;" v-if="auth.error">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">Ошибка!</h3>
                    </div>
                    <div class="modal-title">
                        <p class="modal-title">Неверный логин или пароль!</p>
                    </div>

                </div>
            </div>
        </div>




        <div class="btn-group mb-3 w-100" role-group>
            <button class="btn btn-outline-secondary" @click.prevent="switchForm('login')">Войти</button>
            <button class="btn btn-outline-secondary " @click.prevent="switchForm('register')">Зарегистрироваться</button>
        </div>

        <form @submit.prevent="auth.authentificate(username, password)" v-if="loginFormVisible">

            <div class="form-floating mb-3">
                <input id="floatingInput 1" class="form-control" type="text" placeholder="Имя пользователя"
                    v-model="username">
                <label for="floatingInput 1">Имя пользователя!</label>
            </div>

            <div class="form-floating input-group">
                <input id="floatingInput 2" class="form-control" :type="showPassword ? 'text' : 'password'"
                    placeholder="Имя пользователя" v-model="password">
                <button class="btn btn-outline-secondary" @click.prevent="showHide"><i class="bi bi-eye"></i></button>
                <label for="floatingInput 2">Пароль</label>
            </div>

            <button class="btn btn-outline-dark mt-3 form-control" type="submit">Войти</button>
        </form>

        <form @submit.prevent="auth.registrate(username, password, email)" v-else>
            <div class="form-floating mb-3">
                <input id="floatingInput 3" class="form-control" type="text" placeholder="Имя пользователя"
                    v-model="username">
                <label for="floatingInput 3">Имя пользователя!</label>
            </div>

            <div class="form-floating mb-3">
                <input type="email" class="form-control" id="floatingInput 4" placeholder="Почта" v-model="email">
                <label for="floatingInput 4">Почта</label>
            </div>

            <div class="form-floating input-group">
                <input id="floatingInput 5" class="form-control" :type="showPassword ? 'text' : 'password'"
                    placeholder="Имя пользователя" v-model="password">
                <button class="btn btn-outline-secondary" @click.prevent="showHide"><i class="bi bi-eye"></i></button>
                <button class="btn btn-outline-info" @click.prevent="makePassword">Генерировать пароль</button>
                <label for="floatingInput 5">Пароль</label>
            </div>

            <button class="btn btn-outline-dark mt-3 form-control" type="submit">Зарегистрироваться</button>
        </form>
    </div>
</template>
  

<script>
import { useAuthStore } from "@/store/AuthStore";
import { defineComponent } from "vue";
export default defineComponent({
    setup() {
        const auth = useAuthStore();

        return { auth: auth };
    },
    data() {
        return {
            password: "",
            username: "",
            email: "",
            showPassword: false,
            loginFormVisible: true,
        };
    },
    methods: {
        switchForm(formType) {
            // Метод для переключения между формами
            this.loginFormVisible = formType === 'login';
        },
        // Генерация пароля
        makePassword() {
            const length = Math.floor(Math.random() * (16 - 8 + 1)) + 8; // Минимум 8, максимум 16 символов
            const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            const lowercase = 'abcdefghijklmnopqrstuvwxyz';
            const numbers = '0123456789';
            const specialChars = '@!#';

            let result = '';

            while (result.length < length) {
                const charSet = Math.random() < 0.5 ? uppercase : lowercase;

                // Выбираем случайный символ из выбранного charSet
                const randomChar = charSet[Math.floor(Math.random() * charSet.length)];

                if (result.length === 0 || Math.random() < 0.25) {
                    // Добавляем цифру в 25% случаев
                    result += numbers[Math.floor(Math.random() * numbers.length)];
                } else if (result.length < length) {
                    // Добавляем символ из @!# в остальных случаях
                    result += specialChars[Math.floor(Math.random() * specialChars.length)];
                }

                // Добавляем случайный символ из выбранного charSet
                result += randomChar;
            }

            // Установка сгенерированного пароля в поле password
            if (this.loginFormVisible) {
                this.password = '';
            } else {
                this.password = result;
            }

        },

        showHide() {
            this.showPassword = !this.showPassword;
        },

        modalShowError() {
            if (this.auth.error) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },
        modalShowLoading() {
            if (this.auth.loading) {
                return { modal: 'modal fade show' }
            } else {
                return { modal: 'modal fade' }
            }
        },

    },

    created() {
        // Вызов метода для генерации пароля при создании компонента
        this.makePassword();
    },

})


</script>


