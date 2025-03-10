## How to run:



### db_locally

```
docker build -t db-locally db_locally/.
docker run db-locally
```

The terminal should get a printout like this 
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5500
 * Running on http://172.17.0.2:5500
```

The API is now accessible via the Docker network IP, in this case, `172.17.0.2`
