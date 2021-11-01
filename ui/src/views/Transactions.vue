<template>
  <div class="home">
    <h1 class="title is-title">Transactions</h1>

    <p>{{ shownTransactions.length }} shown transactions</p>
    <p><input type="checkbox" v-model="filter"> Filter Results</p>

    <div v-for="transaction in shownTransactions" :key="transaction.id" class="mb-4">
      <Transaction :transaction="transaction" :categories="categories" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import axios from 'axios'

import Transaction from '@/components/Transaction.vue'

@Component({
  components: {
    Transaction
  }
})
export default class Transactions extends Vue {
  private transactions: any[] = [];
  private categories: any[] = [];
  private filter = false

  private async mounted () {
    this.categories = (await axios.get('/api/categories')).data
    this.transactions = (await axios.get('/api/transactions')).data
  }

  private get shownTransactions () {
    return this.filter
      ? this.transactions.filter(e => !e.category_id)
      : this.transactions
  }
}
</script>
