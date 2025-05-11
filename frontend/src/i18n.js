// src/i18n.js
import { createI18n } from 'vue-i18n'
import en from './lang/en'
import zh from './lang/zh'

const messages = {
    en,
    zh
}

const i18n = createI18n({
    locale: 'zh',  // 默认语言
    fallbackLocale: 'en',
    globalInjection: true,
    legacy: false,
    messages
})

export default i18n