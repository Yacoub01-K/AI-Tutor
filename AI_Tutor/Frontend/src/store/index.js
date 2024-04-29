import { createStore } from 'vuex';
import auth from './auth/index'


export default createStore({
  state: {
    problemDescription: ''
  },
  mutations: {
    setProblemDescription(state, description) {
      state.problemDescription = description;
    }
  },
  actions: {
    updateProblemDescription({ commit }, description) {
      commit('setProblemDescription', description);
    }
  },
  modules: {auth},
});