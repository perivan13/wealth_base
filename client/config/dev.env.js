'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  //ROOT_API: '"https://sms.gitwork.ru"',
  ROOT_API: '"http://localhost:8000"',
  // OCR_API: '"https://sms.gitwork.ru/tess_ocr/api/v1/recognizer/"',
  OCR_API: '"http://0.0.0.0:8001/tess_ocr/api/v1/recognizer/"'
})
