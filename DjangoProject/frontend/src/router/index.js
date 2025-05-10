import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/persons',
    name: 'Persons',
    component: () => import('../views/Persons.vue')
  },
  {
    path: '/persons/:id',
    name: 'PersonDetail',
    component: () => import('../views/PersonDetail.vue'),
    props: true
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('../views/Students.vue')
  },
  {
    path: '/staffs',
    name: 'Staffs',
    component: () => import('../views/Staffs.vue')
  },
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('../views/Courses.vue')
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: () => import('../views/CourseDetail.vue'),
    props: true
  },
  {
    path: '/departments',
    name: 'Departments',
    component: () => import('../views/Departments.vue')
  },
  {
    path: '/programs',
    name: 'Programs',
    component: () => import('../views/Programs.vue')
  },
  // 其他实体的路由可以按需添加
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router