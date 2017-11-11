# Setup with Google Cloud Storage

1. Setup a service account
2. Setup the Google Cloud CLI
3. Create a function

## Assumptions

- You have a Google Cloud Bucket where you are already storing images
- The images in that Google Cloud Bucket are publicly accessible

## Set up a service account

1. Open the list of credentials in the [Google Cloud Platform Console](https://console.cloud.google.com/apis/credentials).

2. Click *Create Credentials* and select *Select Service account key.*

![](/images/service-account-key.png)

3. Click the drop-down box below Service account, then click New service account. Select Project -> Owner (?!). Type in a name for the email address. Any name will do. Use the default service account ID. Select JSON. 

![](/images/new-account.png)

4. Click Create. The file will download. Move it to your working directory and rename it to `client_secrets.json`

![](/images/service-account-success.png)

## Setup the Google Cloud Storage CLI

Install and update the Google Cloud Storage CLI. 

```shell
curl https://sdk.cloud.google.com | bash
exec -l $SHELL #restart your shell
gcloud components update
gcloud components install beta
gcloud init
```

Open `client_secrets.json` and find the service account email address. It looks something like: `childsafe@childsafe-XXXXX.iam.gserviceaccount.com`

Authenticate using the CLI: 

```
gcloud auth activate-service-account [YOUR_SERVICE_EMAIL] --key-file client_secret.json
```

If this goes well, you'll get: 

```
Activated service account credentials for: [YOUR_SERVICE_EMAIL]
````

You can also confirm that all went well by using: 

```

gcloud auth list

````
Set up a Google Cloud Function

Create a new file, `index.js`: 

```js
const querystring = require('querystring');
const http = require('http');

exports.childSafe = function (event, callback) {
  const file = event.data;
  const url = file.mediaLink;

  var postData = querystring.stringify({
    'url' : url,
  });

  console.log("File uploaded: " + url)

  var options = {
    hostname: 'baugues.ngrok.io',
    path: '/receive/media/',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': postData.length
    }

    // hostname: 'tunnel.brooklynhacker.com',
    // path: '/receive/media/',
    // method: 'POST',
    // headers: {
    //   'Content-Type': 'application/x-www-form-urlencoded',
    //   'Content-Length': postData.length
    // }
  };

  var req = http.request(options, (res) => {
    context.log('statusCode:', res.statusCode);

    res.on('data', (d) => {
      context.log("Data", d.toString('utf8'));
    });
  });

  req.write(postData);
  req.end();
  callback();
};

```

Deploy the function: 

```
gcloud beta functions deploy childSafe --trigger-bucket gs://childsafe
```

upload a file: 

```
gsutil cp test.jpg gs://[yourbucketname]
```

----------

Your bucket needs to be publicly readable. If it's not: 

Edit bucket permissions: 

https://cloud.google.com/storage/docs/access-control/making-data-public

- edit permissions
- allUsers to Storage Object Viewer



