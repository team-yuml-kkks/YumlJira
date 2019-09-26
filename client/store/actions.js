// Store all action used in project
import axios from 'axios';
import * as mutations from './mutations';

export default {
    login({commit}, payload) {
        const { username, password, email } = payload

        axios.post('/rest-auth/login/', {
            username: username,
            email: email,
            password: password,
        })
        .then((response) => {
            const { data: {
                token
            }} = response;
            commit('setToken', { token });
        })
        .catch(function (error) {
            console.log(error);
        });
    },
}