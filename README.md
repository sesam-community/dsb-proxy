# DSB Elvirksomheter

A simple service to expose a spreadsheet containing the full list of 'elvirksomheter' from the DSB website.

#### :warning: DISCLAIMER!This is made as a workaround due to a lack of api at this time and should not be considered a reliable source.


Example system config:
----------------------

```json
{
  "_id": "dsb-proxy",
  "type": "system:microservice",
  "connect_timeout": 60,
  "docker": {
    "image": "sesamcommunity/dsb-elvirksomheter",
    "port": 5000
  },
  "read_timeout": 1800
}
```

Example system config using the microservice as a proxy :
--------------------
Using the proxy to read the spreadsheet into Sesam with the [Excel microservice](https://github.com/sesam-community/excel)  

```json
{
  "_id": "dsb",
  "type": "system:microservice",
  "connect_timeout": 60,
  "docker": {
    "environment": {
      "DOWNLOAD_REQUEST_SPEC": {
        "base_url": "http://dsb-proxy:5000/",
        "do_stream": false
      }
    },
    "image": "sesamcommunity/excel",
    "port": 5000
  },
  "read_timeout": 1800
}
```

Example pipe using the two microservices above
----------------------------------------------

```json
{
  "_id": "dsb-elvirksomhet",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "dsb",
    "url": "?ids=1"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"],
        ["add", "rdf:type",
          ["ni", "dsb:Elvirksomhet"]
        ]
      ]
    }
  }
}

```