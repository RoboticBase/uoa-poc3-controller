import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';

import { ItemType, StockType, StateType, DestinationType, PayloadType } from '@/types';
import { defaultStocks, defaultDestinations } from '@/initials';
import { postShipment } from '@/api';

Vue.use(Vuex);

const state: StateType = {
  stocks: [],
  destinations: [],
  selectedDestination: defaultDestinations[0],
  processing: false,
  ordered: [],
  message: '',
  variant: '',
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
      state.message = val.message;
      state.variant = val.variant;
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

    postShipmentAction(_: ActionContext<StateType, StateType>, payload: PayloadType): void {
      postShipment(payload);
    },
  },
  getters: {
    stocks: (state: StateType): Array<StockType> => state.stocks,
    destinations: (state: StateType): Array<DestinationType>  => state.destinations,
    selectedDestination: (state: StateType): DestinationType | undefined  => state.selectedDestination,
    processing: (state: StateType): boolean => state.processing,
    lastOrdered: (state: StateType): PayloadType => state.ordered.slice(-1)[0],
    ordered: (state: StateType): Array<PayloadType> => state.ordered,
    message: (state: StateType): string => state.message,
    variant: (state: StateType): string => state.variant,
  },
  modules: {
  }
});
