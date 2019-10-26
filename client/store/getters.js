// Store all getters used in project
export default {
    /**
     * Return true/false for authorization process.
     * @params {string} token.
     */
    authorizedGrant: ({ token }) => !!token,

    getFormLoginErrors: ({ error_msg: { password, non_field_errors } = {} }) => {
        return {
            password: `${password}`,
            general: `${non_field_errors}`,
        };
    },

    getFormRegisterErrors: ({ error_msg: { username, password1, email, avatar } = {} }) => {
        return {
            username: `${username}`,
            password: `${password1}`,
            email: `${email}`,
            avatar: `${avatar}`,
        };
    },

    /**
     * Get all projects list of loged user.
     * @type { list } project_list.
     */
    getProjects: ( { projects_list = [] }) => projects_list,
}