export type ItemType = {
  id: number;
  title: string;
  image: string;
  category: string;
  reservation: number;
};

export type StockType = ItemType & {
  quantity: number;
  price: number;
};

export type DestinationType = {
  id: number;
  name: string;
  planId: string;
  robotId: string;
};

export type PayloadType = {
  orderDate: string;
  robotId: string;
  planId: string;
  destination: DestinationType;
  items: Array<ItemType>;
  success: () => void;
  failure: (messag: string) => void;
};

export type StateType = {
  stocks: Array<StockType>;
  destinations: Array<DestinationType>;
  selectedDestination: DestinationType;
  processing: boolean;
  ordered: Array<PayloadType>;
  message: string;
  variant: string;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isStock = (item: any): item is StockType => {
  const e: StockType = item as StockType;
  return e.id !== undefined && e.title !== undefined && e.category !== undefined && e.image !== undefined
      && e.quantity !== undefined && e.price !== undefined && e.reservation !== undefined;
};
