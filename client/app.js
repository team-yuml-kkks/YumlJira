import Vue from 'vue';

import App from './App.vue';
import router from './router';

// Import main style files.
import './styles/index.scss';

Vue.config.productionTip = false;

new Vue({
    router,
    render: h => h(App),
}).$mount('#app');
