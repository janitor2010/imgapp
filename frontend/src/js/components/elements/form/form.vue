<template>
  <section>
    <form>
      <div @edited="edited" v-for="prop in model" :is="component(prop)" v-model="item[prop.name]"></div>
    </form>
  </section>
</template>

<script>
import vInput from '@/components/elements/form/elements/input.vue'

export default {
  props: {
    entity: {
      type: String,
      required: false
    },
    item: {
      type: Object,
      required: false
    },
    // id: {
    //   type: [String, Number],
    //   required: false
    // },
  },
  data() {
    return {

    }
  },
  computed: {
    // item() {
    //   return this.$store.state[this.entity].Items.find((el) => {
    //     return (parseInt(el.id) === parseInt(this.id))
    //   })
    // },
    model() {
      return this.$store.state[this.entity].Model;
    }
  },
  methods: {
    component(prop) {
        return (prop.type !== "hidden") ? prop.type : '';
    },
    edited() {
      console.log("input sajhfgshjdfgsjafd");
      if (!this.$store.state[this.entity].EditedItems.some(el => el === this.item))
        this.$store.state[this.entity].EditedItems.push(this.item);
    },
  },
  components: {
      vInput
  },
  mounted() {
  }
};
</script>
