// Store all mutations used in project
export default {
    setToken (state, payload) {
        state.token = payload;
    },

    logout(state) {
        state.token = null;
    }
};