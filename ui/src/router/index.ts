import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

import Transactions from '@/views/Transactions.vue'
import Categories from '@/views/Categories.vue'
import Breakdown from '@/views/Breakdown.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Transactions',
    component: Transactions
  },

  {
    path: '/categories',
    name: 'Categories',
    component: Categories
  },

  {
    path: '/breakdown',
    name: 'Breakdown',
    component: Breakdown
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
