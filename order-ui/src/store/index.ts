import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';

import { ItemType, StockType, StateType, DestinationType, PayloadType } from '@/types';
import { defaultStocks, defaultDestinations } from '@/initials';

Vue.use(Vuex);

const state: StateType = {
  stocks: [],
  destinations: [],
  selectedDestination: defaultDestinations[0],
  processing: false,
  ordered: [],
};

export default new Vuex.Store({
  state: state,
  mutations: {
    listStocks(state: StateType, stocks: Array<StockType>): void {
      state.stocks = stocks;
    },

    updateStock(state: StateType, val: {idx: number; stock: StockType}): void {
      if (state.stocks[val.idx]) {
        state.stocks[val.idx] = val.stock;
      }
    },

    listDestinations(state: StateType, destinations: Array<DestinationType>): void {
      state.destinations = destinations;
    },

    setSelectedDestination(state: StateType, destination: DestinationType): void {
      state.selectedDestination = destination;
    },

    updateProcessing(state: StateType, processing: boolean): void {
      state.processing = processing;
    },

    updateMessage(state: StateType, val: {message: string; variant: string}) {
      // FIX ME
      console.log('message=', val.message, val.variant);
    },

    addOrdered(state: StateType, ordered: PayloadType): void {
      state.ordered.push(ordered);
      ordered.items.forEach((e: ItemType) => {
        const stock = state.stocks.find((s: StockType) => s.id == e.id);
        if (stock !== undefined) {
          stock.quantity -= e.reservation;
          stock.reservation = 0;
        }
      });
    },
  },
  actions: {
    listStocksAction(context: ActionContext<StateType, StateType>): void {
      if (context.state.stocks.length == 0) {
        context.commit('listStocks', defaultStocks);
      }
    },

    listDestinationsAction(context: ActionContext<StateType, StateType>): void {
      if (context.state.destinations.length == 0) {
        context.commit('listDestinations', defaultDestinations);
      }
    },

    postShipmentAction(context: ActionContext<StateType, StateType>, payload: PayloadType): void {
      // FIX ME
      payload.success();
    },
  },
  getters: {
    stocks: (state: StateType): Array<StockType> => state.stocks,
    destinations: (state: StateType): Array<DestinationType>  => state.destinations,
    selectedDestination: (state: StateType): DestinationType | undefined  => state.selectedDestination,
    processing: (state: StateType): boolean => state.processing,
    lastOrdered: (state: StateType): PayloadType => state.ordered.slice(-1)[0],
  },
  modules: {
  }
});
