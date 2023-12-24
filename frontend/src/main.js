// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router';
import { createPinia } from 'pinia';
import AppHeader from './components/AppHeader.vue';
import Chat from './components/Chat.vue';
import './assets/styles.css';



const pinia = createPinia()

const app = createApp(App);

app.component('AppHeader', AppHeader);
app.component('Chat', Chat);

// Используем созданный экземпляр pinia
app.use(pinia);

app.use(router).mount('#app');


