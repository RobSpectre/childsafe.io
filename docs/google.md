# Setup with Google Cloud Storage

1. Setup a service account
2. Setup the Google Cloud CLI
3. Create a function

## Assumptions

- You have a Google Cloud Bucket that stores user generated images
- That bucket is publicly accessible

If that bucket is not accessible, you'll need to go to the bucket list and add `AllUsers` with `Bucket Object Viewer Permissions`. 

![](/images/make-bucket-public.gif)

## Set up a service account

1. Open the [credentials list in the Google Cloud Platform Console](https://console.cloud.google.com/apis/credentials).

2. Click *Create Credentials* and select *Select Service account key.*

![](/images/service-account-key.png)

3. Click the drop-down box below Service account, then click New service account. Select Project -> Owner (?!). Type in a name for the email address. Any name will do. Use the default service account ID. Select JSON. 

![](/images/new-account.png)

4. Click Create. The file will download. 

![](/images/service-account-success.png)

5. Move it to your working directory and rename it to `client_secrets.json`


## Setup the Google Cloud Storage CLI

Install and update the Google Cloud Storage CLI. 

```shell
curl https://sdk.cloud.google.com | bash
exec -l $SHELL #restart your shell
gcloud components update
gcloud components install beta #Functions is in beta
```

On gcloud init: 

2 - Create new configuration

When promoted for email, select the newly created service account. 

Yes when asked to enable cloud resource manager. 

No when asked if you want to enable compute. 

are there flags to say no to turning on compute? 

Open `client_secrets.json` and find the line that says: 

```
"client_email":"childsafe@childsafe-XXXXX.iam.gserviceaccount.com"
```



Use this email address to authenticate the CLI: 

```
gcloud auth activate-service-account [YOUR_SERVICE_EMAIL] --key-file client_secret.json
```

If this goes well, you can run `gcloud auth list` and see the service account. 

## Set up a Google Cloud Function

Now that we have the CLI set up, we can set up a function, and trigger it when a new file uploaded to your Google Cloud Storage bucket. 

Create a new file, `index.js` and paste in this code: 

```js
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
```

Deploy the function: 

```
gcloud beta functions deploy childSafe --trigger-bucket gs://[YOURBUCKETNAME]
```

Once that's complete, upload a file to your bucket to test it out. 

```
gsutil cp test.jpg gs://[YOURBUCKETNAME]
```

----------




