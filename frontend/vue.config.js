module.exports = {
    devServer: {
        port: 8082,  // 前端端口可自定义
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''  // 去掉前缀 /api，使其指向 http://127.0.0.1:8000/
                }
            }
        }
    }
}