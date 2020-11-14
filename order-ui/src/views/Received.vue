<template>
  <div class="received container">
    <div class="d-flex align-items-center justify-content-center h-100">
      <b-button class="float-center receive-btn pl-5 pr-5" @click="receive" v-bind:disabled="processing">受取</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';

import { homeDestination } from '@/initials';
import { PayloadType } from '@/types';

export default Vue.extend({
  name: 'received',
  components: {
  },
  computed: {
    ...mapGetters(['processing']),
  },
  methods: {
    ...mapActions(['postShipmentAction']),

    receive(): void {
      if (this.processing) return;
      const payload: PayloadType = {
        orderDate: (new Date()).toISOString(),
        robotId: homeDestination.robotId,
        planId: homeDestination.planId,
        destination: homeDestination,
        items: [],
        success: (): void => {
          this.$store.commit('updateProcessing', false);
        },
        failure: (message: string): void => {
          console.error('error', message)
          this.$store.commit('updateProcessing', false);
        },
      };
      this.$store.commit('updateProcessing', true);
      this.postShipmentAction(payload);
    },
  }
});
</script>

<style scoped>
.received {
  height: 768px;
}
.receive-btn {
  font-size: 12rem;
}
</style>
