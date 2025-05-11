<template>
  <div class="nav-bar">
    <!-- 左侧 Logo 与标题 -->
    <div class="nav-left">
      <img src="/logo.jpg" alt="Logo" class="logo" />
      <span class="title">DBMS 系统</span>
    </div>

    <!-- 中间菜单栏 -->
    <el-menu
        mode="horizontal"
        :router="true"
        background-color="transparent"
        text-color="#fff"
        active-text-color="#ffd04b"
        class="nav-menu"
    >
      <el-menu-item index="/">{{ $t('home') }}</el-menu-item>
      <el-menu-item index="/departments">{{ $t('departments') }}</el-menu-item>
      <el-menu-item index="/programs">{{ $t('programs') }}</el-menu-item>
      <el-menu-item index="/courses">{{ $t('courses') }}</el-menu-item>
      <el-menu-item index="/students">{{ $t('students') }}</el-menu-item>
      <el-menu-item index="/staffs">{{ $t('staffs') }}</el-menu-item>
    </el-menu>

    <!-- 右侧语言切换 -->
    <div class="lang-buttons">
      <el-button size="small" text @click="switchLang('zh')">中文</el-button>
      <el-button size="small" text @click="switchLang('en')">EN</el-button>
    </div>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n'

export default {
  name: 'NavBar',
  setup() {
    const { locale } = useI18n()
    const switchLang = (lang) => {
      locale.value = lang
    }
    return {
      currentLang: locale,
      switchLang
    }
  }
}
</script>

<style scoped>
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #409EFF;
  padding: 0 20px;
  height: 60px;
  color: white;
}

.nav-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: white;
}

.nav-menu {
  flex: 1;
  justify-content: center;
}

.lang-buttons {
  display: flex;
  gap: 6px;
}
</style>