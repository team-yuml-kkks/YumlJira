<template>
    <div id="Register">
        <div class="columns is-centered">
            <div class="column is-two-fifths register-form">
                <h1>Registration</h1>
                <div class="field">
                    <label class="label">Email</label>
                    <div class="control">
                        <input 
                            class="input"
                            type="email"
                            v-model="email">
                    </div>
                    <div v-if="getFormRegisterErrors.email !== 'undefined'">
                        {{ getFormRegisterErrors.email }}
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
                    <div v-if="getFormRegisterErrors.password !== 'undefined'">
                        {{ getFormRegisterErrors.password }}
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
                <div v-if="getFormRegisterErrors.password !== 'undefined'">
                    {{ getFormRegisterErrors.username }}
                </div>
            </div>
            <div class="file">
                <label class="file-label">
                    <input class="file-input" type="file" id="file" ref="file"
                        v-on:change="fileUpload()">
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
            <div v-if="getFormRegisterErrors.avatar !== 'undefined'">
                {{ getFormRegisterErrors.avatar }}
            </div>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-two-fifths">
                <button class="button is-primary is-pulled-right" 
                    @click="setRegisterData">Register</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapMutations, mapGetters, mapState } from 'vuex';

export default {
    name: 'Register',
    data() {
        return {
            email: undefined,
            password: undefined,
            username: undefined,
            file: null,
        };
    },

    computed: {
        ...mapGetters(['authorizedGrant','getFormRegisterErrors']),
        ...mapState(['error_msg']),
    },

    methods: {
        ...mapMutations({
            setToken: 'setToken',
        }),

        ...mapActions(['userRegister']),

        fileUpload(event) {
            this.file = this.$refs.file.files[0];
        },

        setRegisterData() {
            const registerData = {
                email: this.email,
                password: this.password,
                username: this.username,
                file: this.file,
            }

            this.userRegister(registerData);
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
