<template>
    <div id="ProjectList">
        <div class="container is-fluid">
            <div class="columns">
                <div class="column">
                    <h1>Project list</h1>
                    <ErrorMessages
                        :message="error_msg"/>
                </div>
            </div>
            <div class="columns">
                <div class="column is-one-fifth">
                    <div class="projects-list">
                        <ul id="example-1">
                            <li v-for="project in getProjects" :key="project.pk">
                                {{ project.name }}
                            </li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <button class="button is-primary"
                            @click="userLogout">Logout</button>
                    </div>
                </div>
                <div class="column">
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
            </div>
        </div>
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