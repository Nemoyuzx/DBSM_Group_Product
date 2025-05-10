<template>
  <div class="person-detail">
    <h1>人员详情</h1>
    <p>人员ID: {{ $route.params.id }}</p>
  </div>
</template>

<script>
export default {
  name: 'PersonDetail'
}
</script>

<style scoped>
.person-detail {
  padding: 20px;
}
</style>