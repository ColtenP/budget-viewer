<template>
  <div class="home">
    <h1 class="title is-title">Breakdown</h1>
    <div class="my-4">
      Group By:
      <select class="select" v-model="groupBy" @change="load">
        <option value="month">Month</option>
        <option value="category">Category</option>
      </select>
      Show Subcategory:
      <select class="select" v-model="shownGrouping" @change="shownSubgrouping = null">
        <option v-for="option in availableGroupings" :key="option" :value="option" v-html="option"></option>
      </select>
    </div>

    <v-chart class="chart" :option="shownData" v-if="shownData" @click="selectSubgrouping" />

    <div v-if="shownSubgrouping">
      <h2 class="title is-6" v-html="shownSubgrouping"></h2>
      <p class="mb-4">
        {{ shownTransactions.length }} transactions,
        totalling ${{ shownTransactions.reduce((a, t) => t.amount + a, 0).toFixed(2) }}
        </p>

      <div v-for="transaction in shownTransactions" :key="transaction.id" class="mb-4">
        <Transaction :transaction="transaction" :categories="categories" />
      </div>
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
export default class Breakdown extends Vue {
  private categories: any[] = []
  private breakdown: any = null
  private groupBy: 'month' | 'category' = 'month'
  private shownGrouping: string | null = null
  private shownSubgrouping: string | null = null

  private async created () {
    this.categories = (await axios.get('/api/categories')).data
    this.load()
  }

  private async load () {
    this.shownGrouping = null
    this.shownSubgrouping = null
    this.breakdown = null
    this.breakdown = (await axios.get('/api/breakdown?group_by=' + this.groupBy)).data
    this.shownGrouping = Object.keys(this.breakdown)[0]
  }

  private get console () {
    return console
  }

  private get availableGroupings () {
    return this.breakdown ? Object.keys(this.breakdown) : []
  }

  private selectSubgrouping (data: any) {
    this.shownSubgrouping = data.name
  }

  private get shownData () {
    if (this.shownGrouping && this.breakdown) {
      const option: any = {
        xAxis: {
          data: []
        },
        yAxis: {},
        series: {
          name: 'Spending',
          type: 'bar',
          data: []
        }
      }

      Object.keys(this.breakdown[this.shownGrouping])
        .forEach(name => {
          option.xAxis.data.push(name)
          option.series.data.push(this.breakdown[this.shownGrouping!][name].summary.amount)
        })

      return option
    } else {
      return null
    }
  }

  private get shownTransactions () {
    return this.shownSubgrouping ? this.breakdown[this.shownGrouping!][this.shownSubgrouping].transactions : []
  }
}
</script>

<style lang="scss" scoped>
.chart {
  height: 400px;
}
</style>
