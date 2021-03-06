<template>
  <div class="detail container">
    <Header/>
    <div v-if="stock">
      <SubTitle subtitle=""/>
      <div class="card img-thumbnail">
        <img class="card-img-top" :src="stock.image">
        <div class="card-body px-2 py-3">
          <h5 class="card-title">{{ stock.title }}</h5>
          <p class="card-text">カテゴリ：{{ stock.category }}</p>
          <p class="card-text">価格（税込み）：{{ stock.price }}円</p>
          <p class="card-text">在庫数：{{ stock.quantity }}個</p>
          <p class="card-text form-group">注文数：<input type="number" min="0" :max="stock.quantity" class="form-control reservation" v-model.number="reservation"/></p>
          <p class="mb-0 form-group"><b-button @click="reserve" variant="outline-primary" class="reserve">カートに入れる</b-button></p>
        </div>
      </div>
    </div>
    <Alert/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

import Header from '@/components/Header.vue';
import SubTitle from '@/components/SubTitle.vue';
import Alert from '@/components/Alert.vue';
import { StockType, isStock } from '@/types';

export type DataType = {
  reservation: number;
};

export default Vue.extend({
  name: 'detail',
  components: {
    Header,
    SubTitle,
    Alert,
  },
  data(): DataType {
    return {
      reservation: 0,
    };
  },
  computed: {
    stock(): StockType {
      if (!isStock(this.$route.params.stock)) {
        throw new Error('invalid stock type');
      }
      return this.$route.params.stock;
    },
    idx (): number {
      if (typeof this.$route.params.idx !== 'number') {
        throw new Error('invalid idx type');
      }
      return this.$route.params.idx;
    },
  },
  mounted(): void {
    this.reservation = this.stock.reservation;
  },
  methods: {
    reserve(): void {
      if (this.reservation <= 0) {
        this.$store.commit('updateMessage', {message: '0以下の数は入力できません', variant: 'warning'})
      }
      else if (this.reservation > this.stock.quantity) {
        this.$store.commit('updateMessage', {message: '予約数が在庫数を超えています', variant: 'warning'})
      } else {
        this.stock.reservation = this.reservation;
        this.$store.commit('updateStock', {idx: this.idx, stock: this.stock});
        this.$router.push({name: 'stocks'});
      }
    }
  },
});
</script>
