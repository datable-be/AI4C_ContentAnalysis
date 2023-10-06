# AI4C: Content Analysis Tools

*This API and documentation are currently in development!*

## Quickstart

### Docker

This API runs inside a [Docker](https://www.docker.com/) container, so you need a working installation of the [Docker Engine](https://docs.docker.com/engine/install/). 

Verify your installation with the following command. 

Note that `docker` commands always need to be run with root privileges!

```bash
sudo docker version
```

This should generate a YAML response like this:

```yaml
Client: Docker Engine - Community
 Version:           24.0.6
 API version:       1.43
 Go version:        go1.20.7
 Git commit:        ed223bc
 Built:             Mon Sep  4 12:32:12 2023
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          24.0.6
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.7
  Git commit:       1a79695
  Built:            Mon Sep  4 12:32:12 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.24
  GitCommit:        61f9fd88f79f081d64d6fa3bb1a0dc71ec870523
 runc:
  Version:          1.1.9
  GitCommit:        v1.1.9-0-gccaecfc
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```


### Source code

Download the source code from [Github](https://github.com/datable-be/AI4C_ContentAnalysis):

```bash
git clone https://github.com/datable-be/AI4C_ContentAnalysis
```

### Build and run

Build the Docker image and run the container with the following command (which runs `docker compose up --build` under the hood):

```bash
cd AI4C_ContentAnalysis/development
source build.sh
```

### Test

Verify that the API is accessible with the following command:

```bash
curl http://0.0.0.0:8000/?q=version
```

This should generate a JSON response like this:

```json
{"version":"1.0.1"}
```

## Architecture

### Python virtual environment

This application is developed with a Python [virtual environment](https://docs.python.org/3/library/venv.html), which is part of the Python standard library (since 3.3). A virtual environment is created on top of an existing ("base") Python installation. When used from within a virtual environment, common installation tools such as pip will install Python packages into a virtual environment without needing to be told to do so explicitly. A virtual environment is used to contain a specific Python interpreter and software libraries and binaries which are needed to support a project (library or application). These are by default isolated from software in other virtual environments and Python interpreters and libraries installed in the operating system.

A virtual environment is not considered as movable or copyable – you just recreate the same environment in the target location.

To recreate this virtual environment, be sure to use Python 3.11 (preferably exactly [3.11.5](https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tar.xz)) as the base installation.

Create the virtual environment with the following command (from the project root directory):

```bash
python3 -m venv venv
```

Activate the virtual environment with the following command:

```bash
source venv/bin/activate
```

Install the project pacakages with the following command:
```bash
python3 -m pip install -r development/requirements.txt
```

### Docker

The API itself is containerized with [Docker](https://docs.docker.com/).

The development directory contains a `Dockerfile` for building the container image and a `docker-compose.yml` for running the container.

Both can be done is a single step with the following command:

```bash
sudo docker compose up --build
```

The development directory also contains a shortcut for this command: `build.sh`, while the shortcut `up.sh` can be used to run the container, if you have already built it.

You can list the most recent Docker image builds with the following command:

```bash
sudo docker images
```

The output should contain a line like this:
```text
REPOSITORY               TAG             IMAGE ID       CREATED         SIZE
...
development_ai4c         latest          ef5362fd7d4d   3 hours ago     1.03GB
```

You can list running containers with the following command:

```bash
sudo docker ps
```

```text
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS         PORTS                                       NAMES
6109e06baed2   development_ai4c   "uvicorn --host 0.0.…"   19 minutes ago   Up 9 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   development_ai4c_1
```

### Uvicorn

As seen in the above output, the Docker container now uses [uvicorn](https://www.uvicorn.org/) to serve the API. Uvicorn is an [ASGI](https://asgi.readthedocs.io/en/latest/) (Asynchronous Server Gateway Interface) web server implementation for Python. Alternatives are [Hypercorn](https://pgjones.gitlab.io/hypercorn/) or [Daphne](https://github.com/django/daphne).

For deployment, one can also configure a web server like [Apache](https://httpd.apache.org/) or [NGINX](https://www.nginx.com/) to act as a reverse proxy for the Docker application. In simple terms, a reverse proxy is a server that sits between a client and one or more servers, forwarding client requests to the appropriate server. Using a reverse proxy can provide several benefits, such as improved security, load balancing, and caching.

### FastAPI

The API is built with the [FastAPI](https://fastapi.tiangolo.com/) framework. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

Although there are alternatives (Django REST, Flask), FastAPI is the best choice for the project because of its high [performance](https://fastapi.tiangolo.com/#performance), its type safety with [Pydantic](https://docs.pydantic.dev/latest/), which allows for automatic input validation, and because it is based on (and fully compatible with) the open standards for APIs: [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md) (previously known as Swagger) and [JSON Schema](https://json-schema.org/).

This means FastAPI offers built-in documentation. When you run the container and open your browser at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs), you will see an automatic, interactive, API documentation (integrating [Swagger UI](https://swagger.io/tools/swagger-ui/)): 

![Docs](/doc/img/docs.png "Example of API documentation with Swagger UI")

And because the generated schema is from the OpenAPI standard, there are many compatible tools. Because of this, FastAPI itself provides an alternative API documentation (using [ReDoc](https://redocly.com/redoc/)), which you can access at [http://0.0.0.0:8000/redoc](http://0.0.0.0:8000/redoc):

![ReDoc](/doc/img/redoc.png "Example of API documentation with ReDoc")

You can also directly see the OpenAPI schema at [http://0.0.0.0:8000/openapi.json](http://0.0.0.0:8000/openapi.json).

## Usage

### GET requests

This API accepts a few basic GET requests to get information about the application:

```bash
curl http://0.0.0.0:8000/?q=version
```

Expected output:

```json
{"version":"1.0.1"}
```

and:

```bash
curl http://0.0.0.0:8000/?q=info
```

Expected output:

```json
{"title":"AI4C Content Analysis Tools","summary":"AI4Culture - Content analysis tools","description":"This API offers object and color detection tools for images","termsOfService":"http://www.datable.be/","contact":{"name":"./Datable","url":"http://www.datable.be/","email":"info@datable.be"},"license":{"name":"MIT","url":"https://opensource.org/license/mit/"},"version":"1.0.1"}
```

It also accepts requests to the ``/image`` path to show an annotated image:

```bash
curl -O http://0.0.0.0:8000/image?img=4cc4ff8a39925002a25650a89c5de92fdbfeb011_2.png
```

Please note that these are currently for debugging purposes only and will only be saved if `"debug": true` is set in the `settings.json` file.

![Object detection](/doc/img/object.png "Example of API object detection")

### POST requests

The main usage of the API is via POST requests to the URL paths ``/v1/object`` and/or ``/v1/color``.

Since these are typically longer requests, the software repository contains an example request for both detection tools:

```bash
py3 development/app/examples/object_detect.py
```

Expected output (*current output might differ!*):

```text
POST http://0.0.0.0:8000/v1/object
REQUEST =
{
    "id": "http://example.com/images/123",
    "min_confidence": 0.8,
    "max_objects": 1,
    "source": "http://example.com/images/123.jpg",
    "service": "GoogleVision",
    "service_key": "****"
}
RESPONSE =
{
    "@context": {},
    "@graph": [
        {
            "id": "http://datable.be/color-annotations/123",
            "type": "Annotation",
            "created": "2023-09-30",
            "creator": {
                "id": "https://github.com/hvanstappen/AI4C_object-detector",
                "type": "Software",
                "name": "AI4C object detector"
            },
            "body": [
                {
                    "source": "http://www.wikidata.org/entity/Q200539"
                },
                {
                    "type": "TextualBody",
                    "purpose": "tagging",
                    "value": "dress",
                    "language": "en"
                }
            ],
            "target": {
                "source": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
                "selector": {
                    "type": "FragmentSelector",
                    "conformsTo": "http://www.w3.org/TR/media-frags/",
                    "value": "xywh=percent:87,63,9,21"
                }
            },
            "confidence": 0.8
        },
        {}
    ]
}
```

Or:

```bash
py3 development/app/examples/color_detect.py
```

Expected output (*current output might differ!*):

```text
POST http://0.0.0.0:8000/v1/color
REQUEST =
{
    "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
    "max_colors": 3,
    "min_area": 0.15,
    "foreground_detection": true,
    "selector": {
        "type": "FragmentSelector",
        "conformsTo": "http://www.w3.org/TR/media-frags/",
        "value": "xywh=percent:87,63,9,21"
    },
    "source": "http://example.com/images/123.jpg"
}
RESPONSE =
{
    "@context": {
        "as": "https://www.w3.org/ns/activitystreams#",
        "dc": "http://purl.org/dc/terms/",
        "dce": "http://purl.org/dc/elements/1.1/",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "oa": "http://www.w3.org/ns/oa#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "soa": "http://sw.islab.ntua.gr/annotation/",
        "id": {
            "@id": "@id",
            "@type": "@id"
        },
        "type": {
            "@id": "@type",
            "@type": "@id"
        },
        "value": "rdf:value",
        "created": {
            "@id": "dc:created",
            "@type": "xsd:dateTime"
        },
        "creator": {
            "@id": "dc:creator",
            "@type": "@id"
        },
        "language": "dc:language",
        "Software": "as:Application",
        "name": "foaf:name",
        "Annotation": "oa:Annotation",
        "TextPositionSelector": "oa:TextPositionSelector",
        "TextualBody": "oa:TextualBody",
        "body": {
            "@id": "oa:hasBody",
            "@type": "@id"
        },
        "scope": {
            "@id": "oa:hasScope",
            "@type": "@id"
        },
        "selector": {
            "@id": "oa:hasSelector",
            "@type": "@id"
        },
        "source": {
            "@id": "oa:hasSource",
            "@type": "@id"
        },
        "target": {
            "@id": "oa:hasTarget",
            "@type": "@id"
        },
        "Literal": "soa: Literal "
    },
    "@graph": [
        {
            "id": "http://datable.be/color-annotations/123",
            "type": "Annotation",
            "created": "2023-09-30",
            "creator": {
                "id": "https://github.com/hvanstappen/AI4C_color-detector",
                "type": "Software",
                "name": "AI4C color detector"
            },
            "body": [
                "http://thesaurus.europeanafashion.eu/thesaurus/10403",
                "http://thesaurus.europeanafashion.eu/thesaurus/11098",
                "http://thesaurus.europeanafashion.eu/thesaurus/10404"
            ],
            "target": {
                "source": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081"
            }
        }
    ]
}
```

### Error handling

Error handling for both GET and POST requests is done by FastAPI, as you can see in the following examples.

Invalid URL path:

```bash
curl http://0.0.0.0:8000/invalid_path
```

Expected output:

```json
{"detail":"Not Found"}
```

An invalid query returns an empty response:

```bash
curl http://0.0.0.0:8000/?q=invalid_query
```

Expected output:

```json
{"detail":"Invalid query"}
```

Invalid JSON body in a POST request:

```bash
curl -H "Content-Type: application/json" -X POST -d '{}' http://0.0.0.0:8000/v1/object
```

Expected output:

```json
{"detail":[{"type":"missing","loc":["body","id"],"msg":"Field required","input":{},"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","source"],"msg":"Field required","input":{},"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","service_key"],"msg":"Field required","input":{},"url":"https://errors.pydantic.dev/2.3/v/missing"}]}
```

If, however, there is an error in generating the response, the client will receive an "Internal Server Error" with a HTTP status code 500. We do not catch these, as these are bugs in the code that would otherwise remain undetected. If you notice any such bug, please report it to us via the GitHub [issue tracker](https://github.com/datable-be/AI4C_ContentAnalysis/issues).

## Benchmarks

The following benchmarks were run with [ApacheBench](https://httpd.apache.org/docs/2.4/programs/ab.html) on a local development machine with the following specifications:

```text
Operating system:       Linux Mint 21.2 Cinnamon
Linux Kernel:           5.15.0-78-generic
Processor:              Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz x 4
RAM memory:             15.3 GiB
Hard Drives:            518.3 GB
System:                 Dell XPS 13 9370
``` 

The following command benchmarks 50,000 GET requests with 1,000 concurrent requests:

```bash
ab -k -c1000 -n50000 -S "http://0.0.0.0:8000/?q=version"
```

Output:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0.0.0.0 (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        uvicorn
Server Hostname:        0.0.0.0
Server Port:            8000

Document Path:          /?q=version
Document Length:        19 bytes

Concurrency Level:      1000
Time taken for tests:   45.522 seconds
Complete requests:      50000
Failed requests:        0
Keep-Alive requests:    0
Total transferred:      8150000 bytes
HTML transferred:       950000 bytes
Requests per second:    1098.38 [#/sec] (mean)
Time per request:       910.435 [ms] (mean)
Time per request:       0.910 [ms] (mean, across all concurrent requests)
Transfer rate:          174.84 [Kbytes/sec] received

Connection Times (ms)
              min   avg   max
Connect:        0    10   48
Processing:    39   895 1510
Waiting:        7   709 1404
Total:         67   905 1511

Percentage of the requests served within a certain time (ms)
  50%    848
  66%    883
  75%    952
  80%    981
  90%   1115
  95%   1252
  98%   1410
  99%   1464
 100%   1511 (longest request)
```

The following command benchmarks 50,000 POST requests with 1,000 concurrent requests.

*Please note that the POST request currently yields a dummy request, so these numbers are not yet representative of the real performance.*

```bash
echo '{}' > post.txt
ab -k -p post.txt -T application/json -c1000 -n50000 -S "http://0.0.0.0:8000/v1/object"
rm post.txt
```

Output:

```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0.0.0.0 (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        uvicorn
Server Hostname:        0.0.0.0
Server Port:            8000

Document Path:          /v1/object
Document Length:        394 bytes

Concurrency Level:      1000
Time taken for tests:   44.143 seconds
Complete requests:      50000
Failed requests:        0
Non-2xx responses:      50000
Keep-Alive requests:    0
Total transferred:      27850000 bytes
Total body sent:        8400000
HTML transferred:       19700000 bytes
Requests per second:    1132.69 [#/sec] (mean)
Time per request:       882.853 [ms] (mean)
Time per request:       0.883 [ms] (mean, across all concurrent requests)
Transfer rate:          616.12 [Kbytes/sec] received
                        185.83 kb/s sent
                        801.95 kb/s total

Connection Times (ms)
              min   avg   max
Connect:        0     8   40
Processing:    13   869 1040
Waiting:        1   668  948
Total:         53   877 1054

Percentage of the requests served within a certain time (ms)
  50%    875
  66%    896
  75%    907
  80%    914
  90%    933
  95%    947
  98%    979
  99%   1042
 100%   1054 (longest request)
```

## Analysis

### Object

#### Internal

The built-in object analysis of this API uses the [pre-trained MobileNet-SSD v3 model for object detection](https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API). This model uses the [COCO dataset](https://cocodataset.org/#overview), which consists of 80 classes of images.

Our implementation is inspired by [https://github.com/zafarRehan/object_detection_COCO](https://github.com/zafarRehan/object_detection_COCO).

## Read more

- [Python virtual environments with venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
- [Deploying FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
