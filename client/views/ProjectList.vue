<template>
    <div id="ProjectList">
        <h1>Project list</h1>
        {{ error_msg }}
        <button class="button is-primary is-pulled-right"
            @click="userLogout">Logout</button>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';

export default {
    name: 'ProjectList',

    computed: {
        ...mapGetters(['authorizedGrant']),
        ...mapState(['error_msg']),
    },

    methods: {
        ...mapActions(['userLogout']),
    },

    watch: {
        authorizedGrant() {
            this.$router.replace({ name: 'home' });
        },
    },
}
</script>