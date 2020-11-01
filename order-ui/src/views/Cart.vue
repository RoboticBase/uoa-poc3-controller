<template>
  <div class="cart container">
    <Header/>
    <SubTitle subtitle="カートの内容"/>
    <div class="row">
      <div class="col-sm-6 col-md-3" v-for="item in items" :key="item.id">
        <div class="card img-thumbnail">
          <img class="card-img-top" :src="item.image">
          <div class="card-body px-2 py-3">
            <h5 class="card-title">{{ item.title }}</h5>
            <p class="card-text">カテゴリ：{{ item.category }}</p>
            <p class="card-text">在庫数：{{ parseInt(item.quantity)}}個</p>
            <p class="card-text">注文数：{{ parseInt(item.reservation)}}個</p>
          </div>
        </div>
      </div>
    </div>
    <div v-if="items.length > 0">
      <div>Shipping</div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';

import Header from '@/components/Header.vue';
import SubTitle from '@/components/SubTitle.vue';
import { StockType } from '@/types';

export default Vue.extend({
  name: 'cart',
  components: {
    Header,
    SubTitle
  },
  computed: {
    ...mapGetters(['stocks']),
    items(): boolean {
      return this.stocks.filter((stock: StockType) => {
        return stock.reservation > 0
      });
    },
  },
});
</script>