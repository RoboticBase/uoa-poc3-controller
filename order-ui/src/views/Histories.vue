<template>
  <div class="histories container">
    <Header/>
    <SubTitle subtitle="注文履歴"/>
    <div v-for="(order, idx) in ordered" :key="idx">
      <b-card no-body class="mx-auto">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block href="#" v-b-toggle="'accordion-'+idx" variant="default" class="orderDate">{{ order.orderDate }}のご注文</b-button>
        </b-card-header>
        <b-collapse v-bind:id="'accordion-'+idx" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text class="destination">{{ order.destination.name }}へお届け</b-card-text>
            <div v-for="item in order.items" :key="item.id">
              <b-card-text class="item"><b>{{ item.title}}</b>&nbsp;{{ item.reservation }}個</b-card-text>
            </div>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
    <Alert/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex'

import Header from '@/components/Header.vue';
import SubTitle from '@/components/SubTitle.vue';
import Alert from '@/components/Alert.vue';

export default Vue.extend({
  name: 'histories',
  components: {
    Header,
    SubTitle,
    Alert,
  },
  computed: {
    ...mapGetters(['ordered']),
  },
});
</script>
