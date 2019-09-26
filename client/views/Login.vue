<template>
    <div id="Login">
        <div class="columns is-centered">
            <div class="column is-two-fifths register-form">
                <h1>Login</h1>
                <p class="help is-danger is-size-6"><b>{{ errorMessage }}</b></p>
                <div class="field">
                    <label class="label">Email</label>
                    <div class="control">
                        <input 
                            class="input"
                            type="email"
                            v-model="email">
                    </div>
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
                </div>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-two-fifths">
                <button class="button is-primary is-pulled-right" @click="setUserData">Login</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'Register',
    data() {
        return {
            password: undefined,
            username: undefined,
            email: undefined,
            errorMessage: undefined,
        };
    },

    computed: {
        ...mapGetters(['authorizedGrant']),
    },

    methods: {
        ...mapActions({
            login: 'login',
        }),

        setUserData() {
            const userData = {
                'username': this.username,
                'password': this.password,
                'email': this.email,
            }

            this.login(userData);
        },
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