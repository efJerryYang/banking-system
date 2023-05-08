import { createStore } from 'vuex'

export default createStore({
  state: {
    loggedIn: false,
    sessionId: '',
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
    setUsername(state, username) {
      state.username = username
    },
    setUserType(state, userType) {
      state.userType = userType
    }
  },
  actions: {
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
        commit('setUsername', username)
        commit('setUserType', data.userType) // TODO: not compatible with backend
      }
      return data
    },
    async logout({ commit }, { sessionId }) {
      const response = await fetch('/api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sessionId })
      })
      const data = await response.json()

      console.log('logout', data.message)

      if (data.status === 'success') {
        commit('setLoggedIn', false)
        commit('setSessionId', '')
        commit('setUsername', '')
        commit('setUserType', '')
      }
      return data
    }
  },
  modules: {}
})
