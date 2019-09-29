<template>
    <div id="ProjectList">
        <h1>Project list</h1>
        <button class="button is-primary is-pulled-right"
            @click="userLogout">Logout</button>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';

export default {
    name: 'ProjectList',

    computed: {
        ...mapGetters(['authorizedGrant']),
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