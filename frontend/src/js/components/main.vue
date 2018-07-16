<template>
    <div class="app">
        <main-header/>
        <transition name="fade" mode="out-in">
            <router-view></router-view>
        </transition>
    </div>
</template>
<script>

    import mainHeader from '@/components/layouts/header.vue';
  //  import api from '@/api';

    export default {
        components: {
            mainHeader
        },
        watch: {},
        data() {
            return {

            }
        },
        methods: {},
        created() {
      //    this.initialized = true; //
        },
        mounted() {}
    }
</script>
<style lang="scss" type="text/scss">
</style>
