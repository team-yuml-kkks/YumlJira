// Store all action used in project
import axios from 'axios';

export default {
    userLogin({commit}, payload) {
        const { username, password } = payload

        axios.post('/rest-auth/login/', {
            username: username,
            password: password,
        })
        .then((response) => {
            const { data = {} } = response;

            commit('setUser', { data });
        })
        .catch(function (error) {
            console.log(error);
        });
    },

    userRegister({commit}, payload) {
        const { email, password, username, file } = payload

        let formData = new FormData();

        if (this.file !== null ) {
            formData.append('avatar', file);
        }

        formData.append('username', username);
        formData.append('email', email);
        formData.append('password1', password);
        formData.append('password2', password);

        axios.post('/rest-auth/registration/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then((response) => {
            const { data = {} } = response;
            commit('setUser', { data });
        })
        .catch(function (error) {
            console.log(error.response);
        });
    },

    userLogout({ commit }) {
        axios.post('/rest-auth/logout/', {
        }).then((response) => {
            commit('logout');
        }).catch((error) => {
            console.log(error);
        });
    },
}