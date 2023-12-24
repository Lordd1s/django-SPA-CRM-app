import { RouterLink, createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login-Registration.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Login-Registration.vue')
  },
  {
    path: '/vacancy',
    name: 'Vacancy',
    component: () => import('../views/Vacancy.vue')
  },
  {
    path: '/all_cv',
    name: 'allCv',
    component: () => import('../views/AllCv.vue')
  },
  {
    path: '/create_vacancy',
    name: 'CreateVacancy',
    component: () => import('../views/CreateVacancy.vue')
  },
  {
    path: '/newsletter',
    name: 'Newsletter',
    component: () => import('../components/Newsletter.vue')
  },
  {
    path: '/applications',
    name: 'Applications',
    component: () => import('../components/Applications.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../components/Profile.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
