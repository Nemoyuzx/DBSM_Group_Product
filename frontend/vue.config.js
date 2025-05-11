module.exports = {
  devServer: {
    port: 8082,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django后端地址
        changeOrigin: true
      },
      // 为不带/api前缀的请求也设置代理
      '/table-counts': {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
        pathRewrite: {'^/': '/api/'}
      },
      '/table-data': {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
        pathRewrite: {'^/': '/api/'}
      }
    }
  }
}