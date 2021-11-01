<template>
  <div class="box">
    <article class="media">
      <div class="media-left">
        <span :class="amountClasses">
          ${{ amount }}
        </span>
      </div>

      <div class="media-content">
        <div class="content">
          <p class="is-size-5" v-html="transaction.description"></p>
          Purchased with {{ transaction.source }}
        </div>
      </div>

      <div class="media-right has-text-right">
        <p class="is-size-6" v-html="transaction.date"></p>

        <select v-model="categoryId" :key="transaction.id" class="select mt-2">
          <option v-for="c in categories" :value="c.id" :key="c.id" v-html="c.name"></option>
        </select>
      </div>
    </article>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from 'vue-property-decorator'
import axios from 'axios'
import type { Category, Transaction } from '@/types'

@Component
export default class TransactionComponent extends Vue {
  @Prop({ required: true })
  private transaction!: Transaction

  @Prop({ required: true })
  private categories!: Category[]

  private categoryId: number | null = this.transaction.category_id

  @Watch('categoryId')
  private async onCategoryIdChange (categoryId: number | null) {
    await axios.put('/api/transactions/' + this.transaction.id, { category_id: categoryId })
    Vue.set(this.transaction, 'category_id', categoryId)
  }

  private get amount () {
    return this.transaction.amount.toFixed(2)
  }

  private get amountClasses () {
    return [
      this.transaction.amount <= 0 ? 'has-text-success' : 'has-text-danger',
      'is-size-5'
    ]
  }
}
</script>
