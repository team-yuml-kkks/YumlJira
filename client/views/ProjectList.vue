<template>
    <div id="ProjectList">
        <h1>Project list</h1>
        {{ error_msg }}
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

export default {
    name: 'ProjectList',

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
        ...mapGetters(['authorizedGrant']),
        ...mapState(['error_msg']),
    },

    methods: {
        ...mapActions(['userLogout']),

        updateBlock(id, status) {
            this.blocks.find(b => b.id === Number(id)).status = status;
        },
    },

    watch: {
        authorizedGrant() {
            this.$router.replace({ name: 'home' });
        },
    },
}
</script>