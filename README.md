# AI4C: Content Analysis Tools

*This API and documentation are currently in development!*

## Quickstart

### Docker

This API runs inside a [Docker](https://www.docker.com/) container, so you need a working installation of the [Docker Engine](https://docs.docker.com/engine/install/). Verify your installation with the following command. Notice that `docker` commands always need to be run with root privileges.

```bash
sudo docker info
```

This should generate a YAML response like this:

client: Docker Engine - Community
 Version:    24.0.6
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.11.2
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.21.0
    Path:     /usr/libexec/docker/cli-plugins/docker-compose
  scan: Docker Scan (Docker Inc.)
    Version:  v0.23.0
    Path:     /usr/libexec/docker/cli-plugins/docker-scan

Server:
 Containers: 1
  Running: 1
  Paused: 0
  Stopped: 0
 Images: 11
 Server Version: 24.0.6
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 61f9fd88f79f081d64d6fa3bb1a0dc71ec870523
 runc version: v1.1.9-0-gccaecfc
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 5.15.0-78-generic
 Operating System: Linux Mint 21.2
 OSType: linux
 Architecture: x86_64
 CPUs: 8
 Total Memory: 15.34GiB
 Name: XPS-13-9370
 ID: UNSD:2TZE:5IDV:CPJ3:VVAB:RXVP:XIGT:NBRS:E3WF:ZNVX:HWZT:BVXC
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false


### Source code

Download the source code from [Github](https://github.com/datable-be/AI4C_ContentAnalysis):

```bash
git clone https://github.com/datable-be/AI4C_ContentAnalysis
```

### Build and run

Build the Docker image and run the container with the following command (which runs `docker compose up --build` under the hood):

```bash
cd AI4C_ContentAnalysis/venv/development
source build.sh
```

### Test

Verify that the API is accessible with the following command:

```bash
curl http://0.0.0.0:8000/?q=info
```

This should generate a JSON response like this:

```json
{"title":"AI4C Content Analysis Tools","summary":"AI4Culture - Content analysis tools","description":"This API offers object and color detection tools for images","termsOfService":"http://www.datable.be/","contact":{"name":"./Datable","url":"http://www.datable.be/","email":"info@datable.be"},"license":{"name":"MIT","url":"https://opensource.org/license/mit/"},"version":"1.0.1"}
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

You can list the most recently created Docker images with the following command:

```bash
sudo docker images
```

The output should look like this:
```text
REPOSITORY               TAG             IMAGE ID       CREATED         SIZE
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

As seen in the above output, the Docker container now uses [uvicorn](https://www.uvicorn.org/) to serve the API. Uvicorn is an [ASGI](https://asgi.readthedocs.io/en/latest/), i.e. Asynchronous Server Gateway Interface, web server implementation for Python. 

### FastAPI

The API is built with the [FastAPI](https://fastapi.tiangolo.com/) framework. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

Although there are alternatives (Django REST, Flask), FastAPI is the best choice for the project because of its high [performance](https://fastapi.tiangolo.com/#performance) and bceause it is based on (and fully compatible with) the open standards for APIs: [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md) (previously known as Swagger) and [JSON Schema](https://json-schema.org/).

This means FastAPI offers built-in documentation. When you run the container and open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), you will see an automatic, interactive, API documentation (integrating [Swagger UI](https://swagger.io/tools/swagger-ui/)): 

![Docs](/doc/img/docs.png "Example of API documentation with Swagger UI")

And because the generated schema is from the OpenAPI standard, there are many compatible tools. Because of this, FastAPI itself provides an alternative API documentation (using [ReDoc](https://redocly.com/redoc/)), which you can access at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc):

![ReDoc](/doc/img/docs.png "Example of API documentation with ReDoc")


## Read more

- [Python virtual environments with venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
- [Deploying FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
