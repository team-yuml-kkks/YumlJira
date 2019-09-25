<template>
    <div id="MainPage">
        <router-link :to="{ name: 'register' }">Register</router-link>
        <router-link :to="{ name: 'login' }">Login</router-link>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                name: 'MainPage'
            }
        }
    }
</script>