import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../components/Home.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../components/About.vue')
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
    component: () => import('../views/Applications.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
