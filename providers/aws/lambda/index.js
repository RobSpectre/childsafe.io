'use strict'

const http = require('http')
const querystring = require('querystring')

// const CHILD_SAFE_URL = process.env.CHILD_SAFE_URL

exports.handler = (event, context, callback) => {
  const promises = event.Records.map(record => {
    return new Promise((resolve, reject) => {
      const bucket = record.s3.bucket.name
      const key = record.s3.object.key
      const resource_id = `${record.s3.bucket.arn}/${key}`
      const url = `https://s3.amazonaws.com/${bucket}/${key}`

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
          return reject(new Error(`status code: ${res.statusCode}`))
        }

        res.on('error', err => reject(err))

        res.on('data', chunk => {
          body += chunk
        })

        res.on('end', () => resolve(body))
      })

      req.write(postData)
      req.end()
    })
  })

  Promise.all(promises)
    .then(() => callback(null))
    .catch(err => {
      console.error(err)
      callback(err)
    })
}
