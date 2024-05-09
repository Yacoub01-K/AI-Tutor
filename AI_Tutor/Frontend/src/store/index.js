import { createStore } from 'vuex';
import auth from './auth/index'


export default createStore({
  state: {
    problemDescription: '',
    lessonName: ''
  },
  mutations: {
    setProblemDescription(state, description) {
      state.problemDescription = description;
    },
    setLessonName(state, description) {
      state.lessonName = description;
    }
  },
  actions: {
    updateProblemDescription({ commit }, description) {
      commit('setProblemDescription', description);
    },
    pushLessonName({commit}, description) {
      commit('setLessonName', description);
    }
  },
  modules: {auth},
});