'use strict'

const http = require('http')
const querystring = require('querystring')

module.exports = (context, myBlob) => {
  const url = context.bindingData.uri
  const resource_id = context.bindingData.blobTrigger

  const postData = querystring.stringify({ url, resource_id })

  const options = {
    hostname: 'tunnel.brooklynhacker.com',
    path: '/receive/media/',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': postData.length
    }
  }

  const req = http.request(options, res => {
    let body = ''

    if (res.statusCode !== 201) {
      context.log('statusCode:', res.statusCode)
    }

    res.on('data', chunk => {
      body += chunk
    })

    res.on('end', () => {
      context.log('Data', body)
      context.done()
    })
  })

  req.write(postData)
  req.end()
}
