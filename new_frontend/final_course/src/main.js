import './assets/main.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import AppHeader from './components/AppHeader.vue';
import Chat from './views/Chat.vue';
const app = createApp(App)

app.use(router)

app.use(createPinia())

app.component('AppHeader', AppHeader)
app.component('Chat', Chat)
app.mount('#app')
