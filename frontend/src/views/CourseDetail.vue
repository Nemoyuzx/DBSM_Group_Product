<template>
  <div class="course-detail">
    <h1>课程详情</h1>
    <p>课程ID: {{ $route.params.id }}</p>
  </div>
</template>

<script>
export default {
  name: 'CourseDetail'
}
</script>

<style scoped>
.course-detail {
  padding: 20px;
}
</style>