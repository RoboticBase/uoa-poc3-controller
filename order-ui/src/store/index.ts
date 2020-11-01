import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const defaultStocks = [
  {
    title: "幕の内弁当",
    itemUrl: require("@/assets/obentou_makunouchi.png"),
    quantity: 12,
    unit: "個",
    price: 480,
  },
  {
    title: "ハンバーグ弁当",
    itemUrl: require("@/assets/obentou_hamburg.png"),
    quantity: 10,
    unit: "個",
    price: 450,
  },
  {
    title: "牛丼弁当",
    itemUrl: require("@/assets/obentou_gyudon.png"),
    quantity: 18,
    unit: "個",
    price: 380,
  },
  {
    title: "助六寿司",
    itemUrl: require("@/assets/obentou_sukerokuzushi.png"),
    quantity: 15,
    unit: "個",
    price: 380,
  },
  {
    title: "のり弁当",
    itemUrl: require("@/assets/obentou_nori.png"),
    quantity: 20,
    unit: "個",
    price: 350,
  },
  {
    title: "お茶",
    itemUrl: require("@/assets/petbottle_tea.png"),
    quantity: 40,
    unit: "個",
    price: 150,
  },
  {
    title: "烏龍茶",
    itemUrl: require("@/assets/petbottle_uroncha.png"),
    quantity: 35,
    unit: "個",
    price: 150,
  },
  {
    title: "水",
    itemUrl: require("@/assets/petbottle_water.png"),
    quantity: 21,
    unit: "個",
    price: 110,
  },
]

export default new Vuex.Store({
  state: {
    stocks: [],
  },
  mutations: {
    listStocks(state, stocks) {
      state.stocks = stocks
    },
  },
  actions: {
    listStocksAction(context) {
      if (Array.isArray(context.state.stocks) && context.state.stocks.length == 0) {
        context.commit('listStocks', defaultStocks);
      }
    },
  },
  getters: {
    stocks: (state) => state.stocks,
  },
  modules: {
  }
})
