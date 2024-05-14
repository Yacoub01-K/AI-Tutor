import { createStore } from 'vuex';
import auth from './auth/index'


export default createStore({
  state: {
    problemDescription: '',
    lessonName: '',
    lessonTopic: '',       // Added to hold the topic
    lessonDifficulty: '',
  },
  mutations: {
    setProblemDescription(state, description) {
      state.problemDescription = description;
    },
    setLessonDetails(state, { name, topic, difficulty }) {
      state.lessonName = name;
      state.lessonTopic = topic;
      state.lessonDifficulty = difficulty;
    }
  },
  actions: {
    updateProblemDescription({ commit }, description) {
      commit('setProblemDescription', description);
    },
    updateLessonDetails({ commit }, { name, topic, difficulty }) {
      commit('setLessonDetails', { name, topic, difficulty });
    }
  },
  modules: {auth},
});