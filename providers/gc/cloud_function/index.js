'use strict'

const querystring = require('querystring')
const https = require('https')
const runtimeConfig = require('cloud-functions-runtime-config')

exports.childSafe = function(event, callback) {
  runtimeConfig
    .getVariable('childsafe-runtime-config', 'childsafe_user_id')
    .then(user_id => {
      console.log('event', event)
      const file = event.data
      const url = file.mediaLink
      const resource_id = event.resource

      const postData = querystring.stringify({ url, resource_id, user_id })

      console.log('postData', postData)

      console.log('File uploaded: ' + url)

      const options = {
        hostname: 'childsafe.io',
        path: '/receive/media/',
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Length': postData.length
        }
      }

      const req = https.request(options, res => {
        let body = ''

        if (res.statusCode !== 201) {
          const err = new Error(`status code: ${res.statusCode}`)
          console.error(err)
          return callback(err)
        }

        res.on('error', err => {
          console.error(err)
          return callback(err)
        })

        res.on('data', chunk => {
          body += chunk
        })

        res.on('end', () => {
          console.log(body)
          callback()
        })
      })

      req.write(postData)
      req.end()
    })
    .catch(err => {
      console.error(err)
      return callback(err)
    })
}
