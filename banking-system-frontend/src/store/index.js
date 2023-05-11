import { createStore } from 'vuex'

const store =  createStore({
  state: {
    loggedIn: false,
    sessionId: localStorage.getItem('sessionId') || '',
    accountId: '',
    username: '',
    userType: ''
  },
  mutations: {
    setLoggedIn(state, loggedIn) {
      state.loggedIn = loggedIn
    },
    setSessionId(state, sessionId) {
      state.sessionId = sessionId
    },
    setAccountId(state, accountId) {
      state.accountId = accountId
    },
    setUsername(state, username) {
      state.username = username
    },
    setUserType(state, userType) {
      state.userType = userType
    }
  },
  actions: {
    setStoreFromLocalStorage({ commit }) {
      const sessionId = localStorage.getItem('sessionId')
      const username = localStorage.getItem('username')
      const userType = localStorage.getItem('userType')
      if (sessionId && username && userType) {
        commit('setLoggedIn', true)
        commit('setSessionId', sessionId)
        commit('setUsername', username)
        commit('setUserType', userType)
      }
    },
    async login({ commit }, { username, password, clientId }) {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, clientId })
      })
      const data = await response.json()

      console.log('login', data.message)

      if (data.status === 'success') {
        commit('setLoggedIn', true)
        commit('setSessionId', data.sessionId)
        commit('setAccountId', data.accountId)
        commit('setUsername', username)
        commit('setUserType', data.userType)
        localStorage.setItem('sessionId', data.sessionId)
        localStorage.setItem('username', username)
        localStorage.setItem('userType', data.userType)
      }
      return data
    },
    async logout({ commit }) {
      const sessionId = this.state.sessionId
      console.log('logout', sessionId)
      if (!sessionId) {
        return { status: 'error', message: 'Not logged in' }
      }
      commit('setLoggedIn', false)
      commit('setSessionId', '')
      commit('setAccountId', '')
      commit('setUsername', '')
      commit('setUserType', '')
      localStorage.removeItem('sessionId')
      localStorage.removeItem('username')
      localStorage.removeItem('userType')
      try {
        const response = await fetch('/api/logout', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${sessionId}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()

        console.log('logout', data.message)
        return data
      } catch (error) {
        console.log(error)
        localStorage.removeItem('sessionId')
        localStorage.removeItem('username')
        localStorage.removeItem('userType')
        return { status: 'error', message: 'Not logged in' }
      }
    },
    // TODO: not compatible with backend
    async getUserType({ commit }) {
      const response = await fetch('/api/getUserType', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      const data = await response.json()
      console.log('getUserType', data.message)
      if (data.status === 'success') {
        commit('setUserType', data.userType)
      }
      return data
    }
  },
  modules: {}
})

export default store