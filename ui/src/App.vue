<template>
  <div id="app" class="container">
    <div id="nav" class="py-4 has-text-centered">
      <router-link to="/">Transactions</router-link> |
      <router-link to="/categories">Categories</router-link> |
      <router-link to="/breakdown">Breakdown</router-link>
    </div>
    <router-view/>
  </div>
</template>
