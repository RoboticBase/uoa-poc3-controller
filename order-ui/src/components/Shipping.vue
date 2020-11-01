<template>
  <div class="shipping container">
    <div class="row form-group">
      <div class="col-sm-8">
        <label for="destination">お届け先:</label>
        <select id="destination" class="form-control" @change="setSelectedDestination($event.target.value)">
          <option v-for="destination in destinations" :key="destination.id" v-bind:value="destination.id">{{ destination.name }}</option>
        </select>
      </div>
      <div class="col-sm-4 align-self-end">
        <b-button variant="primary" class="float-right order" @click="shipping" v-bind:disabled="processing">注文</b-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';

import { ItemType, StockType, PayloadType } from '@/types';

export default Vue.extend({
  name: 'shipping',
  created(): void {
    this.listDestinationsAction();
  },
  computed: {
    ...mapGetters(['stocks', 'destinations', 'selectedDestination', 'processing']),
  },
  methods: {
    ...mapActions(['listDestinationsAction', 'postShipmentAction']),

    setSelectedDestination(destinationId: number): void {
      this.$store.commit('setSelectedDestination', this.destinations[destinationId]);
    },

    shipping(): void {
      if (this.processing) return
      const items: Array<ItemType> = this.stocks.filter((stock: StockType) => {
        return stock.reservation > 0;
      }).map((stock: StockType) => {
        return {
          id: stock.id,
          title: stock.title,
          image: stock.image,
          category: stock.category,
          reservation: stock.reservation
        };
      });

      if (this.selectedDestination !== undefined && items.length > 0) {
        const payload: PayloadType = {
          orderDate: (new Date()).toISOString(),
          robotId: this.selectedDestination.robotId,
          planId: this.selectedDestination.planId,
          destination: this.selectedDestination,
          items: items,
          success: (): void => {
            this.$store.commit('addOrdered', payload);
            this.$store.commit('updateProcessing', false);
            this.$router.push({name: 'ordered'});
          },
          failure: (message: string): void => {
            this.$store.commit('updateMessage', {message: message, variant: 'danger'})
            this.$store.commit('updateProcessing', false);
          },
        };
        this.$store.commit('updateMessage', {message: '処理中', variant: 'info'})
        this.$store.commit('updateProcessing', true);
        this.postShipmentAction(payload)
      } else {
        this.$store.commit('updateMessage', {message: 'お届け先と商品を選択してください', variant: 'warning'})
      }
    },
  },
});
</script>
