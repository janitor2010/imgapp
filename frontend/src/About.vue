<template>
  <div>
    <h1>{{ msg }}</h1>
  aboutr
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
    filesChange(fieldName, fileList) {
      console.log("changes",fieldName,fileList);
      const formData = new FormData();

      if (!fileList.length) return;

      // append the files to FormData
      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          formData.append(fieldName, fileList[x], fileList[x].name);
        });

        axios.post("http://127.0.0.1:5000/", formData)
          // get data
          .then(x => {
            console.log("res",x);
          })
    }
  }
}
</script>

<style lang="scss">

</style>
