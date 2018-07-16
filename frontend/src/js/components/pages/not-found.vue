<template>
  <div>
    <h1>{{ msg }}</h1>
    ERORORORORO
    <router-link :to="'/'">home</router-link>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      uploadFieldName: 'files'
    }
  },
  methods: {
  }
}
</script>

<style lang="scss">

</style>
