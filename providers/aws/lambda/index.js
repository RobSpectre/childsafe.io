'use strict'

const request = require('request')

const CHILD_SAFE_URL = process.env.CHILD_SAFE_URL

exports.handler = (event, context, callback) => {
  const promises = event.Records.map(record => {
    return new Promise((resolve, reject) => {
      const bucket = record.s3.bucket.name
      const key = record.s3.object.key
      const resource_id = `${record.s3.bucket.arn}/${key}`
      const url = `https://s3.amazonaws.com/${bucket}/${key}`

      request.post(
        CHILD_SAFE_URL,
        { form: { url, resource_id } },
        (err, res, body) => {
          if (err) {
            return reject(err)
          }
          if (res.statusCode !== 201) {
            return reject(body)
          }
          resolve()
        }
      )
    })
  })

  Promise.all(promises)
    .then(() => callback(null))
    .catch(err => {
      console.error(err)
      callback(err)
    })
}
