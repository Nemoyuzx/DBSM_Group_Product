import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue';
import AllTables from '../views/AllTables.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('../views/Courses.vue')
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: () => import('../views/CourseDetail.vue')
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
    path: '/persons/:id',
    name: 'PersonDetail',
    component: () => import('../views/PersonDetail.vue')
  },
  {
    path: '/all-tables',
    name: 'AllTables',
    component: AllTables
  },
  {
    path: '/table-data/:tableName',
    name: 'TableDataView',
    component: () => import('../views/TableDataView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router