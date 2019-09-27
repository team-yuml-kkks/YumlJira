// Store all mutations used in project
export default {
    setUser (state, { data }) {
        const {
            token,
            user: {
                pk, email, username,
            },
        } = data;

        state.token = token;
        state.pk = pk;
        state.email = email;
        state.username = username;
    },

    logout(state) {
        state.token = null;
        state.pk = undefined;
        state.email = undefined;
        state.username = undefined;
    }
};