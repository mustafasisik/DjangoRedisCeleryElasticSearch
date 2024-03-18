
## Running The Project

1. **Build necessary images and containers**

- Build nginx image

``` bash
docker build -t djelastic:test ./djelastic
```

- Run all containers except workers for dev
``` bash
docker-compose -f docker-compose.yml up
```
or
``` bash
docker-compose -f docker-compose.yml up -d
```
prometheus grafana will be added later.

2. **Run a group of celery workers with a determined server running on a "textgen" queue**
#### RUN A GROUP OF CELERY WORKERS WITH A DETERMINED SERVER RUNNING ON "textgen" queue
