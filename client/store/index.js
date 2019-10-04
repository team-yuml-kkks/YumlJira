import Vue from 'vue';
import Vuex from 'vuex';

import state from './state';
import mutations from './mutations';
import getters from './getters';
import actions from './actions';

import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex);

const store =  new Vuex.Store({
    state,
    mutations,
    getters,
    actions,

    plugins: [createPersistedState()]
});

export default store;