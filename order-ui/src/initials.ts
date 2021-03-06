import { StockType, DestinationType} from '@/types';

export const defaultStocks: Array<StockType> = [
  {
    id: 0,
    title: "幕の内弁当",
    category: "お弁当",
    image: require("@/assets/obentou_makunouchi.png"),
    quantity: 12,
    price: 480,
    reservation: 0,
  },
  {
    id: 1,
    title: "ハンバーグ弁当",
    category: "お弁当",
    image: require("@/assets/obentou_hamburg.png"),
    quantity: 10,
    price: 450,
    reservation: 0,
  },
  {
    id: 2,
    title: "牛丼弁当",
    category: "お弁当",
    image: require("@/assets/obentou_gyudon.png"),
    quantity: 18,
    price: 380,
    reservation: 0,
  },
  {
    id: 3,
    title: "助六寿司",
    category: "お弁当",
    image: require("@/assets/obentou_sukerokuzushi.png"),
    quantity: 15,
    price: 380,
    reservation: 0,
  },
  {
    id: 4,
    title: "のり弁当",
    category: "お弁当",
    image: require("@/assets/obentou_nori.png"),
    quantity: 20,
    price: 350,
    reservation: 0,
  },
  {
    id: 5,
    title: "お茶",
    category: "飲み物",
    image: require("@/assets/petbottle_tea.png"),
    quantity: 40,
    price: 150,
    reservation: 0,
  },
  {
    id: 6,
    title: "烏龍茶",
    category: "飲み物",
    image: require("@/assets/petbottle_uroncha.png"),
    quantity: 35,
    price: 150,
    reservation: 0,
  },
  {
    id: 7,
    title: "水",
    category: "飲み物",
    image: require("@/assets/petbottle_water.png"),
    quantity: 21,
    price: 110,
    reservation: 0,
  },
];

export const defaultDestinations: Array<DestinationType> = [
  {
    id: 0,
    name: "ガレージ3",
    planId: "plan01",
    robotId: "robot01",
  },
  {
    id: 1,
    name: "ガレージ2",
    planId: "plan01",
    robotId: "robot01",
  },
];

export const homeDestination: DestinationType = {
  id: 9,
  name: "ホーム",
  planId: "plan01r",
  robotId: "robot01",
};
