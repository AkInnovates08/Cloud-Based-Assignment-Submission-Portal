# Failure Handling

| Failure | Response |
|---|---|
| Upload fails | Keep metadata uncommitted; show retry option |
| DB unavailable | Return 503, log incident, retry safe operations |
| Storage unavailable | Do not create a completed submission record without the file |
| Token expires | Return 401; frontend asks user to log in again |
| Duplicate submission request | Use assignment/student uniqueness or idempotency key |
| Internet drops | Client retries only when safe; show upload progress/error |
| Backend fails | Stateless replacement instance handles future requests |

## Idempotency

A submission should have a client-generated request ID or server-side uniqueness rule so a double-click does not create two logical submissions. File upload and metadata creation should be treated as a small workflow with explicit compensation if the second step fails.
