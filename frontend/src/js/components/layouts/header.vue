<template>
    <header>
      <router-link :key="index" v-for='item, index in menu' :to='item.link'>
        <svg-icon v-if="item.icon" :type="item.icon"></svg-icon>
        <span v-else>{{ item.name }}</span>
      </router-link>
    </header>
</template>
<script>

    import svgIcon from '@/components/elements/svg-icon.vue'

    export default {
        components: {
          svgIcon
        },
        watch: {},
        data() {
            return {
                menu: [
                  {
                    link: '/',
                    name: 'Главная',
                    icon: 'home-interface'
                  },
                  {
                    link: '/image-classification',
                    name: 'Image classification',
                  },
                  {
                    link: '/object-detection',
                    name: 'Object detection',
                  }
                ]
            }
        },
        methods: {},
        created() {
      //    this.initialized = true;
        },
        mounted() {}
    }
</script>
<style lang="scss" type="text/scss" scoped>
    header {
      display: flex;
      justify-content: center;
      height: 100px;
      align-items: flex-end;

      a {
        display: inline-block;
        margin: 0 20px;
      }
    }
</style>
