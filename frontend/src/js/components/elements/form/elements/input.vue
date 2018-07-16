<template>
  <div class="form-group">
    <input :value="value" @input="$emit('input', $event.target.value);$emit('edited')" type="text" name="" placeholder="FFF" >
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: [String, Number],
      required: false
    },
  },
  methods: {
  },
};
</script>
