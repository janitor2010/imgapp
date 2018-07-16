import'../scss/main.scss'
import Vue from 'vue'
import router from '@/router';
import { store } from '@/store';
import mainComponent from '@/components/main.vue';

const files = require.context('!svg-sprite-loader!../images/svg', false, /.*\.svg$/);
files.keys().forEach(files);

new Vue({
  el: '#app',
  router,
  store,
  components: { mainComponent },
  template: '<main-component />',
//  render: h => h(App)
});
