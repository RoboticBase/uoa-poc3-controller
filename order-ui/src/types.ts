export type StockType = {
  id: number;
  title: string;
  category: string;
  image: string;
  quantity: number;
  price: number;
  reservation: number;
};

export type StateType= {
  stocks: Array<StockType>;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isStock = (item: any): item is StockType => {
  const e: StockType = item as StockType;
  return e.id !== undefined && e.title !== undefined && e.category !== undefined && e.image !== undefined
      && e.quantity !== undefined && e.price !== undefined && e.reservation !== undefined;
};
