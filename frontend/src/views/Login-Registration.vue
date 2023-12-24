<template>
    <div class="size my-5 p-3 bg-light-subtle rounded">

        <div class="btn-group mb-3" role-group>
            <button class="btn btn-outline-secondary" @click.prevent="switchForm('login')">Войти</button>
            <button class="btn btn-outline-secondary " @click.prevent="switchForm('register')">Зарегистрироваться</button>
        </div>

        <form @submit.prevent="authentificate" v-if="loginFormVisible">

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

        <form @submit.prevent="registrate" v-else>
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
  
<style scoped>
.size {
    margin: auto;
    max-width: 500px;
    overflow: hidden;
}
</style>
  

<script>
import axios from "axios";
import { authStore } from "@/store/store";
import { onMounted, defineComponent } from "vue";
export default defineComponent ({
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

        async authentificate() {
            try {
                const response = await axios.post(
                    'http://127.0.0.1:8000/api/token/',
                    {
                        username: this.username,
                        password: this.password
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                );
                localStorage.setItem('accessToken', response.data.access);
                localStorage.setItem('refreshToken', response.data.refresh);
                
                authStore().setUsername(this.username);
                console.log(this.username)
                
                this.$router.push({ name: 'Home' });
                setTimeout(() => {
                    window.location.reload();
                }, 1000); 

            } catch (error) {
                console.error('Authentication failed:', error);
                alert("Неверный логин или пароль!");
            }
        },

        async registrate() {
            try {
                const request = await axios.post(
                    'http://127.0.0.1:8000/registrate/',
                    {
                        username: this.username,
                        password: this.password,
                        email: this.email
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    }
                );
                console.log(request)
                alert('Регистрация прошла успешно! Можете войти в систему!');
                this.$router.push({ name: 'Login' });
            } catch (error) {
                alert(error);
            }
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

    },


    created() {
        // Вызов метода для генерации пароля при создании компонента
        this.makePassword();
    },

})


</script>


