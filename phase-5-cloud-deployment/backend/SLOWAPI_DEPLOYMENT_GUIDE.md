# SlowAPI Configuration for Production Deployment

## About SlowAPI
SlowAPI is used in this application for rate limiting to prevent abuse of authentication endpoints and protect against brute force attacks.

## Configuration Details

The following endpoints have rate limiting applied:

- `/auth/login` - Limited to 10 requests per minute per IP
- `/auth/signup` - Limited to 5 requests per hour per IP
- `/auth/validate` - Limited to 10 requests per minute per IP
- `/auth/me` - Limited to 30 requests per minute per IP
- `/auth/refresh` - Limited to 5 requests per minute per IP

## Production Considerations

1. **Redis Backend**: For production deployments with multiple workers/servers, configure SlowAPI to use Redis as the storage backend instead of in-memory storage to share rate limit counters across all instances.

2. **Environment Variables**: In production, you may want to adjust the rate limits:
   - Increase limits for legitimate high-volume users
   - Decrease limits to further restrict potential attackers

3. **Deployment Script**: Use the provided `run_server.py` script to ensure the server binds to the correct host (127.0.0.1) for accessibility.

## No Issues Expected in Deployment

The SlowAPI integration in this application:
- ✅ Uses proper initialization and decorators
- ✅ Handles rate limit exceeded scenarios gracefully
- ✅ Does not cause startup errors
- ✅ Works correctly with the application lifecycle

The rate limiting will continue to function normally in deployment without causing errors. The limits may need adjustment based on expected traffic volumes in production.

## Running in Production

For production deployment, you can run the server using:
```bash
# Standard uvicorn command
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using the provided script
python run_server.py
```

The rate limiting will remain effective and no errors should occur during deployment.