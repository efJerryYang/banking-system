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
  actions: {},
  modules: {}
})
