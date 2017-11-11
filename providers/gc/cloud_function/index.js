'use strict'

const querystring = require('querystring')
const http = require('http')

exports.childSafe = function(event, callback) {
  const file = event.data
  const url = file.mediaLink
  const resource_id = event.id

  const postData = querystring.stringify({ url, resource_id })

  console.log('File uploaded: ' + url)

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
      console.error(`status code: ${res.statusCode}`)
    }

    res.on('data', chunk => {
      body += chunk
    })

    res.on('end', ()=> {
      console.log(body)
      callback()
    })
  })

  req.write(postData)
  req.end()
}
