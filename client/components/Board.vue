<template>
    <div id="Board">
        <kanban-board :stages="getStages" :blocks="blocks" @update-block="updateBlock">
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
import { mapGetters, mapState } from 'vuex';

export default {
    name: 'Board',

    data() {
        return {
            blocks: [
                {
                id: 1,
                status: 'Done',
                title: 'Done',
                },
            ],
        };
    },

    computed: {
        ...mapGetters(['getProjectDetail', 'getStages']),
    },

    methods: {
        updateBlock(id, status) {
            this.blocks.find(b => b.id === Number(id)).status = status;
        },
    },
}
</script>