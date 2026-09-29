# Scalability

## 10 students
One small API instance, SQLite/local storage, or one managed database and object bucket is enough.

## 1,000 students
Use managed PostgreSQL, object storage, stateless FastAPI instances, connection pooling, indexes, and a CDN for frontend assets.

## 100,000 students
Use:
- CDN + static frontend
- API gateway/load balancer
- horizontally scaled/stateless API
- managed PostgreSQL with pooling/read replicas as needed
- object storage for files
- signed URLs so large files bypass the API
- Redis/cache for frequently requested assignment metadata
- queue + worker for virus scanning, notifications, thumbnails, analytics
- monitoring, rate limiting and autoscaling

### Deadline spike scenario

If 100,000 students submit near a deadline, the API should not proxy every large file through one server. Instead:
1. authenticate the student,
2. issue a short-lived upload permission/signed URL,
3. upload directly to object storage,
4. write small metadata to the database,
5. process scanning asynchronously,
6. use a queue for downstream work.

This separates compute traffic from file bandwidth and prevents the API from becoming the bottleneck.
