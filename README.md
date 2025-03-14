# CachingProxy
```
CachingProxy from [roadmap.sh](https://roadmap.sh/projects/caching-server) with fastapi and redis <br/>
Fast api runs at port 80 and forward any GET request to http://dummyjson.com
```

# How to run
```
docker-compose up
```

# Testing
```
curl http://localhost:80/some/hahaball

Output -> INFO:app.main:X-Cache: MISS

curl http://localhost:80/some/hahaball again

Output -> INFO:app.main:X-Cache: HIT
```

