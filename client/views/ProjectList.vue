<template>
    <div id="ProjectList">
        <div class="container is-fluid">
            <div class="columns">
                <div class="column">
                    <h1>Project list</h1>
                    <ErrorMessages
                        :message="error_msg"/>
                    <button @click="clearSelectedProjectDetail()">Clear</button>
                </div>
            </div>
            <div class="columns">
                <div class="column is-one-fifth">
                    <div class="projects-list">
                        <ul id="example-1">
                            <li v-for="project in getProjects" :key="project.pk">
                                <a type="button" class="button project-btn"
                                    @click="selectProjectDetails(project.pk)">{{ project.name }}</a>
                            </li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <button class="button is-primary"
                            @click="userLogout">Logout</button>
                    </div>
                </div>
                <div class="column">
                    <template v-if="getProjectDetail">
                        <Board/>
                    </template>
                    <template v-else>
                        <h1>some info</h1>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';

import Board from '../components/Board.vue';
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
        ...mapGetters(['authorizedGrant', 'getProjects', 'getProjectDetail']),
        ...mapState(['error_msg', 'projectDetail']),
    },

    methods: {
        ...mapActions(['userLogout', 'projectsList', 'selectProjectDetails', 'clearSelectedProjectDetail',]),

        updateBlock(id, status) {
            this.blocks.find(b => b.id === Number(id)).status = status;
        },
    },

    components: {
        Board,
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