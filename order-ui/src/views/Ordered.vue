<template>
  <div class="ordered container">
    <Header/>
    <div v-if="lastOrdered">
      <SubTitle subtitle="注文完了"/>
      <p class="msg">注文を受け付けました。配送ロボット（{{ lastOrdered.robotId }}）が商品を配送します。</p>
      <p class="msg">注文日時：{{ lastOrdered.orderDate }}</p>
      <p class="msg">お届け先：{{ lastOrdered.destination.name }}</p>
      <p class="msg">お届けする商品</p>
      <div class="row">
        <div class="col-sm-6 col-md-3" v-for="item in lastOrdered.items" :key="item.id">
          <div class="card img-thumbnail">
            <img class="card-img-top" :src="item.image">
            <div class="card-body px-2 py-3">
              <h5 class="card-title">{{ item.title }}</h5>
              <p class="card-text">カテゴリ：{{ item.category }}</p>
              <p class="card-text">注文数：{{ parseInt(item.reservation) }}個</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';

import Header from '@/components/Header.vue';
import SubTitle from '@/components/SubTitle.vue';

export default Vue.extend({
  name: 'ordered',
  components: {
    Header,
    SubTitle
  },
  computed: {
    ...mapGetters(['lastOrdered']),
  },
});
</script>
