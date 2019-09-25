<template>
    <div id="ProjectList">
        <h1>Project list</h1>
        <button class="button is-primary is-pulled-right" @click="logout">Logout</button>
    </div>
</template>

<script>
import axios from 'axios';
import { mapMutations, mapState, mapGetters } from 'vuex';

export default {
    name: 'ProjectList',
    data() {
        return {
        };
    },

    computed: {
        ...mapGetters(['authorizedGrant']),
    },

    methods: {
        ...mapMutations(['logout']),
    },

    watch: {
        authorizedGrant() {
            this.$router.replace({ name: 'home' });
        },
    },
}
</script>