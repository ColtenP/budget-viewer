<template>
  <div>
    <h1 class="title is-1">Transaction Categories</h1>

    <Category v-for="category in categories" :category="category" :key="category.id" />

    <hr/>

    <div class="box">
      <form @submit.prevent="onCreate">
        <div class="field">
          <label class="label">Category</label>
          <input type="text" class="input" v-model="category">
        </div>

        <div class="buttons is-right">
          <button class="button is-primary">Create</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import axios from 'axios'

import Category from '@/components/Category.vue'

@Component({
  components: {
    Category
  }
})
export default class Categories extends Vue {
  private categories: any[] = [];
  private category = ''

  private async mounted () {
    this.categories = (await axios.get('/api/categories')).data
  }

  private async onCreate () {
    await axios.post('/api/categories', { name: this.category })
    this.category = ''
    this.categories = (await axios.get('/api/categories')).data
  }
}
</script>
