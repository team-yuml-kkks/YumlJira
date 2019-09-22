import Vue from 'vue';
import Router from 'vue-router';

import MainPage from './views/MainPage.vue';
import Register from './views/Register.vue';
import Login from './views/Login.vue';
import ProjectList from './views/ProjectList.vue';

Vue.use(Router);

const router = new Router({
    mode: 'history',
    routes: [
        { path: '/', name: 'home', component: MainPage },
        { path: '/register', name: 'register', component: Register },
        { path: '/login', name: 'login', component: Login },
        { path: '/project-list', name: 'project-list', component: ProjectList },
    ],
});

export default router;
