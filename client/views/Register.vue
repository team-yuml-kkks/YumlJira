<template>
    <div id="Register">
        <div class="columns is-centered">
            <div class="column is-two-fifths register-form">
                <h1>Registration</h1>
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
                    <label class="label">Password</label>
                    <div class="control">
                        <input 
                            class="input"
                            type="password"
                            v-model="password">
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
            <div class="file">
                <label class="file-label">
                    <input class="file-input" type="file" id="file" ref="file" v-on:change="fileUpload()">
                    <span class="file-cta">
                    <span class="file-icon">
                        <i class="fas fa-upload"></i>
                    </span>
                    <span class="file-label">
                        Choose a file…
                    </span>
                    </span>
                </label>
            </div>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-two-fifths">
                <button class="button is-primary is-pulled-right" @click="register">Register</button>
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
            email: undefined,
            password: undefined,
            username: undefined,
            file: null,
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

        fileUpload(event) {
            this.file = this.$refs.file.files[0];
        },

        register() {
            let formData = new FormData();
            formData.append('file', this.file);

                axios.post('/rest-auth/registration/', {
                    headers:{'Content-Type': 'multipart/form-data'},
                    username: this.username,
                    email: this.email,
                    password1: this.password,
                    password2: this.password,
                    avatar: null,
                })
                .then((response) => {
                    this.setToken(response.data.token);
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
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