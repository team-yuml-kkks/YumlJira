// Store all getters used in project
export default {
    /**
     * Get token for authorization process.
     * @params {boolean} token.
     */
    authorizedGrant: ({ token }) => !!token,
}