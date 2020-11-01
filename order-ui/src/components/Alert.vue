<template>
  <div class="alert container">
    <b-alert
      :show="dismissCountDown"
      :variant="variant"
      dismissible
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >
      {{ message }}
    </b-alert>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';

export type DataType = {
  dismissSecs: number;
  dismissCountDown: number;
};

export default Vue.extend({
  name: 'alert',
  data(): DataType {
    return {
      dismissSecs: 5,
      dismissCountDown: 0
    };
  },
  computed: {
    ...mapGetters(['message', 'variant'])
  },
  methods: {
    countDownChanged(dismissCountDown: number): void {
      this.dismissCountDown = dismissCountDown;
      if (this.dismissCountDown == 0) {
        this.$store.commit('updateMessage', {message: '', variant: ''});
      }
    },
  },
  watch: {
    message(newValue: string): void {
      if (newValue) {
        this.dismissCountDown = this.dismissSecs;
      }
    },
  }
});
</script>
