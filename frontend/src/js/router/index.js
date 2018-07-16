import Vue from 'vue';
import VueRouter from 'vue-router'
import ImgApp from '@/components/pages/imgapp.vue'
import ObjDet from '@/components/pages/objdet.vue'
import Home from '@/components/pages/home.vue'
import Test from '@/components/pages/test.vue'
import NotFound from '@/components/pages/not-found.vue'

Vue.use(VueRouter);

const routes = [
  { path: '/image-classification', component: ImgApp, name: 'imgapp' },
  { path: '/object-detection', component: ObjDet, name: 'objdet' },
  { path: '/', component: Home, name: 'home' },
  { path: '/testAll', component: Test, name: 'testAll' },
  { path: '/test-:id', component: Test, name: 'test', props: (route) => ({ id: route.params.id }) },
  { path: '*', component: NotFound, name: 'error' }
]

const router = new VueRouter({
  routes, // short for `routes: routes`
  mode: 'history'
})


export default router;
