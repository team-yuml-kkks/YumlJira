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
    },

    setError(state, { data }) {
        state.error_msg = data;
    },

    clearErrors(state) {
        state.error_msg = {};
    },

    /**
     * Add to state all projects from api.
     * @param {object} results
     */
    projects(state, { results }) {
        state.projectsList = results;
    },

    setProjectDetail(state, { data }) {
        state.projectDetail = data;
    },

    /**
     * Clear all data of project.
     */
    clearProject(state) {
        state.projectsList = [];
        state.projectDetail = [];
    },

    /**
     * Clear data only of selected project details.
     */
    clearProjectDetail(state) {
        state.projectDetail = {};
    },

    /**
     * Set all columns title to stages array,
     * for vue-kanban component.
     */
    setProjectDetailColumn(state, data) {
        state.stages = data;
    },

    setTasks(state, data) {
        state.tasks = data;
    },
}; 