import Vue from 'vue';
import Vuex from 'vuex';

import { StockType, StateType } from '@/types';
import { defaultStocks } from '@/initials';

Vue.use(Vuex);

const state: StateType = {
  stocks: [],
};

export default new Vuex.Store({
  state: state,
  mutations: {
    listStocks(state, stocks: Array<StockType>): void {
      state.stocks = stocks;
    },

    updateStock(state, val: {idx: number; stock: StockType}): void {
      if (state.stocks[val.idx]) {
        state.stocks[val.idx] = val.stock;
      }
    },
  },
  actions: {
    listStocksAction(context): void {
      if (context.state.stocks.length == 0) {
        context.commit('listStocks', defaultStocks);
      }
    },
  },
  getters: {
    stocks: (state) => state.stocks,
  },
  modules: {
  }
});
