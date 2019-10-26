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
        .catch((error) => {
            
            const { response: {
                data
            } } = error;

            commit('setError', { data })
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
        .catch((error) => {
            const { response: {
                data
            } } = error;

            commit('setError', { data })
        });
    },

    userLogout({ commit }) {
        axios.post('/rest-auth/logout/', {
        }).then((response) => {
            commit('logout');
        }).catch((error) => {
            const { response: {
                data
            } } = error;

            commit('setError', { data });
        });
    },

    /**
     * Gets all projects to loged user.
     * Projects are filtered by add pk of user.
     * Action gets user pk from local state.
     */
    projectsList({ state: { pk } = undefined , commit }) {
        axios.get('/projects/?created_by='+pk)
        .then((response) => {
            const { data: { results } = {} } = response;
            commit('projects', { results });
        })
        .catch((error) => {
            //TODO add handler for error response.
            const { response: {
                data
            } } = error;

            commit('setError', { data });
        });
    }
}