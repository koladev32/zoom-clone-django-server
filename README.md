# zoom-clone-django-server
## How to use the code

**Clone the sources**

```bash
$ git clone https://github.com/koladev32/zoom-clone-django-server.git
$ cd zoom-clone-django-server
```

**Create a virtual environment**

```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

**Install dependencies** using pip

```bash
$ pip install -r requirements.txt
```

**Start the API server** 

```bash
$ python manage.py migrate
$ python manage.py runserver
```

The API server will start using the default port `8000`.


<br />

### [Docker](https://www.docker.com/) execution
---

> Get the code

```bash
$ git clone https://github.com/koladev32/zoom-clone-django-server.git
$ cd zoom-clone-django-server
```

> Start the app in Docker

```bash
$ docker-compose up -d --build
```

Visit `http://localhost:8009` in your browser. The API server will be running.
