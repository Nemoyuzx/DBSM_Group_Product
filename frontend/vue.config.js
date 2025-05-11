module.exports = {
  devServer: {
    port: 8082,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django后端地址
        changeOrigin: true,
        pathRewrite: null // 移除可能导致问题的重写配置
      },
      '/table-counts': {
        target: 'http://localhost:8000', // 直接指向后端根地址
        changeOrigin: true
      },
      '/table-data': {
        target: 'http://localhost:8000', // 直接指向后端根地址
        changeOrigin: true
      }
    }
  }
}