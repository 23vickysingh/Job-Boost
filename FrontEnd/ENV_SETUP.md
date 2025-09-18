# Environment Configuration

## API URL Configuration

The frontend uses environment variables to configure the backend API URL.

### Local Development

For local development, create a `.env.local` file in the `FrontEnd` directory:

```bash
VITE_API_URL=http://localhost:8000
```

### Production Deployment

For production, create a `.env.production` file or set the environment variable:

```bash
VITE_API_URL=https://your-production-backend-url.com
```

### Environment Files Priority

Vite loads environment files in this order:

1. `.env.production` (production build)
2. `.env.local` (always loaded, ignored by git)
3. `.env` (default)
4. `.env.example` (template only)

### Setting Up

1. Copy `.env.example` to `.env.local` for local development
2. Update `VITE_API_URL` with your backend URL
3. The frontend will automatically use the configured URL

### Verification

When running in development mode, the console will show:
```
🔗 API URL configured: http://localhost:8000
```

### Note

- All environment variables for Vite must be prefixed with `VITE_`
- Environment files are git-ignored for security
- The application falls back to `http://localhost:8000` if no URL is configured