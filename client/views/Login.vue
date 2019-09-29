<template>
    <div id="Login">
        <div class="columns is-centered">
            <div class="column is-two-fifths register-form">
                <h1>Login</h1>
                <div v-if="getFormLoginErrors.non_field_errors !== 'undefined'">
                    {{ getFormLoginErrors.non_field_errors }}
                </div>
                <div class="field">
                    <label class="label">Username</label>
                    <div class="control">
                        <input 
                            class="input"
                            type="text"
                            v-model="username">
                    </div>
                </div>
                <div class="field">
                    <label class="label">Password</label>
                    <div class="control">
                        <input 
                            class="input"
                            type="password"
                            v-model="password">
                    </div>
                    <div v-if="getFormLoginErrors.password !== 'undefined'">
                        {{ getFormLoginErrors.password }}
                    </div>
                </div>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-two-fifths">
                <button class="button is-primary is-pulled-right"
                    @click="userLogin({ username, password })">Login</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';

export default {
    name: 'Login',
    data() {
        return {
            password: undefined,
            username: undefined,
        };
    },

    computed: {
        ...mapGetters(['authorizedGrant', 'getFormLoginErrors']),
    },

    methods: {
        ...mapActions(['userLogin']),
    },

    watch: {
        authorizedGrant(value) {
            if (value) {
                this.$router.replace({ name: 'project-list' });
            }
        }
    }
}
</script>