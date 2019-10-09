import Vue from 'vue';

import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios'
import vueKanban from 'vue-kanban'

// Import main style files.
import './styles/index.scss';

Vue.use(vueKanban);

Vue.config.productionTip = false;
Vue.prototype.$http = axios;

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');
