# ucsc-jobs-api

Gathers all the latest information of available positions at UCSC. I built this primarily to practice using Python and Golang in development.

## Requirements

- [Golang](https://golang.org/dl/) v1.11.3^
- [Python](https://www.python.org/downloads/windows/) v3.7^
- [Pipenv](https://github.com/pypa/pipenv)

## Installation

```javascript
git clone https://github.com/anthonydevelops/ucsc-jobs-api.git
cd /ucsc-jobs-api

// Get go dependencies
go get -u github.com/gorilla/mux

// Install web scraper dependencies & run it
cd /lib
pipenv install --dev
pipenv run python jobs.py (for latest json info)
cd ..

// Build server & run it
go build
./ucsc-jobs-api.exe
```

## Endpoints

### Get All Jobs

```
GET /jobs
```

### Get Non-workstudy Jobs

```
GET /jobs/nonworkstudy
```

### Get Workstudy Jobs

```
GET /jobs/workstudy
```

### Get A Specific Job

```
GET /jobs/{title}
```
