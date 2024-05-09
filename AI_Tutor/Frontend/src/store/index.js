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
    setLessonName(state, lessonName) {
      state.lessonName = lessonName;
    }
  },
  actions: {
    updateProblemDescription({ commit }, description) {
      commit('setProblemDescription', description);
    },
    updateLessonName({ commit }, lessonName) {
      commit('setLessonName', lessonName);
    }
  },
  modules: {auth},
});