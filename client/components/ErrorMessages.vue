/**
 * Shows errors text from store if those exist.
 * @param {array} errors_messages
*/
<template functional>
    <div v-if="props.message.length">
        {{ props.message }}
    </div>
</template>
