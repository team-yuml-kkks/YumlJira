<template>
    <div id="ProjectList">
        <h1>Project list</h1>
        <ErrorMessages
            :message="error_msg"/>
        <ul id="example-1">
            <li v-for="project in getProjects" :key="project.pk">
                {{ project.name }}
            </li>
        </ul>
        <button class="button is-primary is-pulled-right"
            @click="userLogout">Logout</button>

        <kanban-board :stages="stages" :blocks="blocks" @update-block="updateBlock">
            <div v-for="block in blocks" :slot="block.id" :key="block.id">
                <div>
                    <strong>id:</strong> {{ block.id }}
                </div>
                <div>
                    {{ block.title }}
                </div>
            </div>
        </kanban-board>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';

import ErrorMessages from '../components/ErrorMessages.vue';
export default {
    name: 'ProjectList',
    // TODO All shit of vue-kanban move to store.
    data() {
        return {
            stages: ["on-hold", "in-progress", "needs-review", "approved"],
            blocks: [
                {
                id: 1,
                status: 'on-hold',
                title: 'Test',
                },
            ],
        };
    },

    computed: {
        ...mapGetters(['authorizedGrant', 'getProjects']),
        ...mapState(['error_msg']),
    },

    methods: {
        ...mapActions(['userLogout', 'projectsList']),

        updateBlock(id, status) {
            this.blocks.find(b => b.id === Number(id)).status = status;
        },
    },

    components: {
        ErrorMessages,
    },

    watch: {
        authorizedGrant() {
            this.$router.replace({ name: 'home' });
        },
    },

    mounted() {
        //Activate axios get a project list from api.
        this.projectsList();
    },
}
</script>