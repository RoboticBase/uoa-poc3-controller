<template>
  <div class="subtitle container">
    <div class="row">
      <div class="col-8 my-auto">
        <span class="subtitle">{{ subtitle }}</span>
      </div>
      <div class="col">
        <b-button :to="{ name: 'stocks'}" variant="outline-default" class="float-right back">戻る</b-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'subtitle',
  props: ['subtitle'],
  data: function () {
    return {}
  },
});
</script>

<style scoped>
.subtitle {
  font-size: 1.2em;
}
</style>