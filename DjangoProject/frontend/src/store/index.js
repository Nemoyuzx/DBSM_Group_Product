import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    persons: [],
    students: [],
    staffs: [],
    courses: [],
    departments: [],
    programs: [],
    loading: false,
    error: null
  },
  getters: {
    getPersonById: (state) => (id) => {
      return state.persons.find(person => person.person_id === parseInt(id))
    },
    getCourseById: (state) => (id) => {
      return state.courses.find(course => course.course_code === id)
    }
  },
  mutations: {
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_PERSONS(state, persons) {
      state.persons = persons
    },
    SET_STUDENTS(state, students) {
      state.students = students
    },
    SET_STAFFS(state, staffs) {
      state.staffs = staffs
    },
    SET_COURSES(state, courses) {
      state.courses = courses
    },
    SET_DEPARTMENTS(state, departments) {
      state.departments = departments
    },
    SET_PROGRAMS(state, programs) {
      state.programs = programs
    },
    ADD_PERSON(state, person) {
      state.persons.push(person)
    },
    UPDATE_PERSON(state, updatedPerson) {
      const index = state.persons.findIndex(p => p.person_id === updatedPerson.person_id)
      if (index !== -1) {
        state.persons.splice(index, 1, updatedPerson)
      }
    },
    DELETE_PERSON(state, personId) {
      state.persons = state.persons.filter(p => p.person_id !== personId)
    }
    // 其他实体的增删改变更可以按需添加
  },
  actions: {
    // 通用的获取数据列表方法
    async fetchItems({ commit }, { endpoint, mutation }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await axios.get(endpoint)
        commit(mutation, response.data.results || response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message || '获取数据失败')
        console.error('Error fetching data:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    // 获取人员列表
    fetchPersons({ dispatch }) {
      return dispatch('fetchItems', { 
        endpoint: 'persons/', 
        mutation: 'SET_PERSONS' 
      })
    },
    // 获取学生列表
    fetchStudents({ dispatch }) {
      return dispatch('fetchItems', { 
        endpoint: 'students/', 
        mutation: 'SET_STUDENTS' 
      })
    },
    // 获取教职工列表
    fetchStaffs({ dispatch }) {
      return dispatch('fetchItems', { 
        endpoint: 'staffs/', 
        mutation: 'SET_STAFFS' 
      })
    },
    // 获取课程列表
    fetchCourses({ dispatch }) {
      return dispatch('fetchItems', { 
        endpoint: 'courses/', 
        mutation: 'SET_COURSES' 
      })
    },
    // 获取部门列表
    fetchDepartments({ dispatch }) {
      return dispatch('fetchItems', { 
        endpoint: 'departments/', 
        mutation: 'SET_DEPARTMENTS' 
      })
    },
    // 获取项目列表
    fetchPrograms({ dispatch }) {
      return dispatch('fetchItems', { 
        endpoint: 'programs/', 
        mutation: 'SET_PROGRAMS' 
      })
    },
    // 获取单个实体详情
    async fetchItemDetail({ commit }, { endpoint, id }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await axios.get(`${endpoint}${id}/`)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message || '获取详情失败')
        console.error('Error fetching detail:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    // 创建新实体
    async createItem({ commit }, { endpoint, data, mutation }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await axios.post(endpoint, data)
        if (mutation) {
          commit(mutation, response.data)
        }
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message || '创建失败')
        console.error('Error creating item:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    // 更新实体
    async updateItem({ commit }, { endpoint, id, data, mutation }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await axios.put(`${endpoint}${id}/`, data)
        if (mutation) {
          commit(mutation, response.data)
        }
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.message || '更新失败')
        console.error('Error updating item:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    // 删除实体
    async deleteItem({ commit }, { endpoint, id, mutation }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        await axios.delete(`${endpoint}${id}/`)
        if (mutation) {
          commit(mutation, id)
        }
        return true
      } catch (error) {
        commit('SET_ERROR', error.message || '删除失败')
        console.error('Error deleting item:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  modules: {
  }
})