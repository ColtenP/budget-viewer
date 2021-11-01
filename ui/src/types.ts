/* eslint-disable camelcase */
export type Transaction = {
  id: number;
  date: string;
  amount: number;
  description: string;
  category_id: number | null;
  source: string;
}

export type BreakdownTransaction = Transaction | {
  month: string;
  category_name: string;
}

export type Category = {
  id: number;
  name: string;
}
