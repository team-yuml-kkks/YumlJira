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
                <button class="button is-primary is-pulled-right" @click="login">Login</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapMutations, mapState, mapGetters } from 'vuex';

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
        ...mapMutations({
            setToken: 'setToken',
        }),

        login() {
            if (!this.username || !this.password) {
                this.errorMessage = "Fill all fields"
            } else {
                axios.post('/rest-auth/login/', {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                })
                .then((response) => {
                    this.setToken(response.data.token);
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
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