<template>
  <div class="box">{{ category.id }} - {{ category.name }}</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class Category extends Vue {
  @Prop({ required: true })
  private category!: any
}
</script>
