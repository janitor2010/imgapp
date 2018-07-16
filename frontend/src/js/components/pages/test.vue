<template>
  <section>
    test
    <ul>
      <router-link :to="{ name: 'test', params: { id: i.id} }" v-for="i in items"> {{ i.name }} </router-link>
    </ul>
    <h2>Childs</h2>
    <ul>
      <li v-for="ch in childs">{{ ch.id }}</li>
    </ul>
    <v-form :entity="entity" :item="item"></v-form>
    <h2>Childs form</h2>
    <v-form v-for="ch in childs" :entity="entity" :item="ch"></v-form>
    {{ $store.state }}
    <br />
    <br />
    <button @click="addChild">Добавить чайлд</button>
    <button @click="saveAll">SaveAll</button>
    <router-link :to="{ name: 'test', params: { id: 22} }">22222</router-link>
  </section>
</template>

<script>
import vForm from '@/components/elements/form/form.vue'

export default {
  props: {
    id: {
      type: [Number,String],
      required: false
    },
  },
  data () {
    return {
  //      id: 1,
        entity: 'Comments'
    }
  },
  computed: {
      items() {
        return this.$store.state[this.entity].Items.filter(el => {
          return (!el.parentId)
        });
      },
      childs() {
        return this.$store.state[this.entity].Items.filter(el => {
          return (el.parentId == this.id)
        });
      },
      item() {
        return this.$store.state[this.entity].Items.find((el) => {
            return (parseInt(el.id) === parseInt(this.id))
          })
      }
  },
  components: {
      vForm
  },
  methods: {
    saveAll() {
        console.log("saveAlls", this.$store.state[this.entity].EditedItems);
        this.$store.state[this.entity].EditedItems = [];
    },
    chooseItem(item) {
      this.id=item.id;
      this.$store.state[this.entity].EditedItemsIds = [];
    },
    addChild() {
      let child = this.$store.state[this.entity].Model.reduce((res, curr) => {
        res[curr.name] = '';
        return res;
      }, {});
      child.parentId = this.id;
      this.$store.state[this.entity].Items.push(child)
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
