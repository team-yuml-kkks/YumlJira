import Vue from 'vue';
import Router from 'vue-router';

import store from './store';
import MainPage from './views/MainPage.vue';
import Register from './views/Register.vue';
import Login from './views/Login.vue';
import ProjectList from './views/ProjectList.vue';

Vue.use(Router);

const router = new Router({
    routes: [
        { path: '/', name: 'home', component: MainPage, },
        {
            path: '/register',
            name: 'register',
            component: Register,
            beforeEnter: async (to, from, next) => {
                await Vue.nextTick();
                const { getters: { authorizedGrant } } = store;
                console.log(authorizedGrant);
                if (authorizedGrant) {
                    next({ name: 'project-list', replace: true });
                } else {
                    next();
                }
            },
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            beforeEnter: async (to, from, next) => {
                await Vue.nextTick();
                const { getters: { authorizedGrant } } = store;
                console.log(authorizedGrant);
                if (authorizedGrant) {
                    next({ name: 'project-list', replace: true });
                } else {
                    next();
                }
            },
        },
        {
            path: '/project-list',
            name: 'project-list',
            component: ProjectList,
            beforeEnter: async (to, from, next) => {
                await Vue.nextTick();
                const { getters: { authorizedGrant } } = store;

                if (authorizedGrant) {
                    next();
                } else {
                    next({ name: 'login', replace: true });
                }
            },
        },
    ],
});
export default router;
