# Elasticsearch API Key Setup Guide

This guide explains how to set up Elasticsearch with API key authentication for the Job Boost application.

## Two Configuration Options

### Option 1: Local Development (No Authentication)
For quick local development, you can disable Elasticsearch security:

1. In `docker-compose.yml`, set:
   ```yaml
   environment:
     - xpack.security.enabled=false
   ```

2. Leave `ELASTICSEARCH_API_KEY` empty in `.env`

### Option 2: Production Setup (API Key Authentication)
For production or secure development:

## Step 1: Start Services
```bash
docker-compose up -d postgres elasticsearch redis
```

## Step 2: Wait for Elasticsearch to be Ready
Check the logs to ensure Elasticsearch is fully started:
```bash
docker-compose logs elasticsearch
```

Wait until you see messages like:
- "started"
- "Cluster health status changed from [YELLOW] to [GREEN]"

## Step 3: Generate API Key
Run the Python script to generate an API key:
```bash
cd BackEnd
python generate_elasticsearch_api_key.py
```

This will output something like:
```
🔑 API Key generated successfully!
==================================================
API Key ID: abc123
API Key Secret: xyz789
Encoded API Key: YWJjMTIzOnh5ejc4OQ==
==================================================

📝 Add this to your .env file:
ELASTICSEARCH_API_KEY=YWJjMTIzOnh5ejc4OQ==
```

## Step 4: Update .env File
Add the generated API key to your `.env` file:
```
ELASTICSEARCH_API_KEY=YWJjMTIzOnh5ejc4OQ==
```

## Step 5: Restart Backend
```bash
docker-compose restart backend
```

## Testing the Setup

### Test Elasticsearch Connection
```bash
# Without API key (if security disabled)
curl http://localhost:9200/_cluster/health

# With API key
curl -H "Authorization: ApiKey YWJjMTIzOnh5ejc4OQ==" http://localhost:9200/_cluster/health
```

### Test from Python
```python
from elasticsearch import Elasticsearch

# With API key
es = Elasticsearch(
    ["http://localhost:9200"],
    api_key="YWJjMTIzOnh5ejc4OQ=="
)

print(es.info())
```

## API Key Features

The generated API key has permissions for:
- **Cluster**: Monitor cluster health
- **Indices**: Full access to `user_profiles` and `resumes` indices
  - Create, read, write, delete documents
  - Create and manage indices

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use different API keys for different environments**
3. **Rotate API keys regularly**
4. **Use minimal required permissions**
5. **Monitor API key usage**

## Troubleshooting

### "Connection refused" Error
- Ensure Elasticsearch is running: `docker-compose ps elasticsearch`
- Check logs: `docker-compose logs elasticsearch`

### "Authentication failed" Error
- Verify API key is correct in `.env`
- Ensure `xpack.security.enabled=true` in docker-compose.yml
- Regenerate API key if needed

### "Index not found" Error
- The application will automatically create indices on first use
- Check Elasticsearch logs for index creation messages

## Manual API Key Management

### List API Keys
```bash
curl -u elastic:changeme http://localhost:9200/_security/api_key
```

### Revoke API Key
```bash
curl -u elastic:changeme -X DELETE http://localhost:9200/_security/api_key/abc123
```

### Create API Key Manually
```bash
curl -u elastic:changeme -X POST "http://localhost:9200/_security/api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "job-boost-backend",
    "role_descriptors": {
      "job_boost_role": {
        "cluster": ["monitor"],
        "indices": [
          {
            "names": ["user_profiles", "resumes"],
            "privileges": ["create", "read", "write", "delete", "index"]
          }
        ]
      }
    }
  }'
```
