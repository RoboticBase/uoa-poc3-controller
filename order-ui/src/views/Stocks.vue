<template>
  <div class="stocks container">
    <Header/>
    <div v-if="stocks.length == 0">
      <span class="text-center empty-stock">読込中</span>
    </div>
    <div v-else class="row">
      <div class="col-sm-6 col-md-3" v-for="(stock, idx) in stocks" :key="stock.id">
        <div class="card img-thumbnail">
          <img class="card-img-top" :src="stock.image">
          <div class="card-body px-2 py-3">
            <h5 class="card-title">{{ stock.title }}</h5>
            <p class="card-text">
              価格（税込み）: {{ stock.price }}円<br/>
              在庫数：{{ stock.quantity }}個
            </p>
            <p class="mb-0"><b-button :to="{ name: 'detail', params: { stock: stock,  idx: idx}}">詳細</b-button></p>
          </div>
        </div>
      </div>
    </div>
    <Alert/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';

import Header from '@/components/Header.vue';
import Alert from '@/components/Alert.vue';

export default Vue.extend({
  name: 'Stocks',
  components: {
    Header,
    Alert,
  },
  created(): void {
    this.listStocksAction();
  },
  computed: {
    ...mapGetters(['stocks']),
  },
  methods: {
    ...mapActions(['listStocksAction']),
  }
});
</script>
