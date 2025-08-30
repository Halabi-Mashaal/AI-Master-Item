# Render Deployment Configuration for MDM-Enhanced AI Agent

## Environment Variables Required for Render

### Core Application Settings
```
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here
USE_LIGHTWEIGHT_NLP=true
MEMORY_OPTIMIZATION=true
```

### Master Data Management (MDM) Settings
```
# Oracle EBS Integration (Optional - will use mock mode if not provided)
ORACLE_HOST=your-oracle-ebs-host
ORACLE_PORT=1521
ORACLE_SERVICE=ORCL
ORACLE_USER=apps
ORACLE_PASSWORD=your-oracle-password

# MDM Features
ENABLE_MDM=true
DATA_QUALITY_THRESHOLD=0.85
AUTO_SYNC_ENABLED=true
```

### Optional Performance Settings
```
MAX_WORKERS=2
WORKER_CONNECTIONS=100
TIMEOUT=30
```

## Build Configuration

### Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Start Command
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 30 src.app:app
```

## Render Service Settings

### Service Type: Web Service
- **Runtime**: Python 3
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 30 src.app:app`
- **Plan**: Starter (512MB RAM should be sufficient with optimizations)

### Auto-Deploy: Yes
- Connected to GitHub repository
- Branch: main
- Auto-deploy on push: Enabled

## Memory Optimization Features

The application includes several memory optimizations for cloud deployment:

1. **Lightweight NLP Mode**: Uses TextBlob instead of heavy transformers
2. **SQLite In-Memory Cache**: For MDM data without persistent storage overhead
3. **Mock Oracle Mode**: Falls back to mock mode if Oracle client unavailable
4. **Lazy Loading**: Libraries loaded only when needed
5. **Memory Monitoring**: Automatic fallback to lightweight modes

## Deployment Health Checks

After deployment, verify functionality with these endpoints:

### Health Check
```
GET https://your-app.onrender.com/health
```
Expected response should include:
```json
{
  "status": "healthy",
  "features": {
    "master_data_management": "enabled",
    "oracle_ebs_integration": "enabled",
    "advanced_nlp": "lightweight"
  }
}
```

### MDM Dashboard
```
GET https://your-app.onrender.com/api/mdm/dashboard
```

### Chat Interface Test
```
POST https://your-app.onrender.com/chat
{
  "message": "What is Master Data Management?"
}
```

## Feature Availability in Cloud

### ✅ Available Features
- Complete MDM functionality (items, suppliers, customers)
- AI-powered data quality assessment
- Bulk import from Excel files
- Data quality dashboard
- Natural language chat interface (Arabic/English)
- REST API endpoints
- SQLite in-memory caching

### ⚠️ Limited Features
- **Oracle EBS Integration**: Requires proper Oracle client setup
  - Falls back to mock mode if Oracle client unavailable
  - Set `USE_MOCK_ORACLE=true` to force mock mode
- **Heavy NLP Models**: Uses lightweight alternatives for memory efficiency

### 🔧 Mock Mode Capabilities
When Oracle client is unavailable, the system operates in mock mode:
- All MDM operations work normally
- Data stored in SQLite cache
- Simulated Oracle EBS synchronization
- Full API functionality maintained
- Quality assessment and validation active

## Troubleshooting

### Common Issues and Solutions

1. **Memory Errors**
   - Set `USE_LIGHTWEIGHT_NLP=true`
   - Reduce worker count: `--workers 1`
   - Enable memory optimization: `MEMORY_OPTIMIZATION=true`

2. **Oracle Connection Issues**
   - System automatically falls back to mock mode
   - Verify environment variables if real Oracle needed
   - Check Oracle client installation

3. **Import Errors**
   - All imports have fallback mechanisms
   - Check logs for specific missing dependencies
   - Use health check endpoint to verify feature availability

4. **Performance Issues**
   - Monitor memory usage via health endpoint
   - Adjust worker configuration
   - Enable caching options

## Expected Deployment Timeline

1. **Build Phase**: 3-5 minutes
   - Install dependencies
   - Compile Python packages
   - Set up environment

2. **Deploy Phase**: 1-2 minutes
   - Start application
   - Initialize MDM system
   - Run health checks

3. **Ready**: Total ~5-7 minutes

## Post-Deployment Verification

1. **Access Web Interface**: Visit your Render URL
2. **Test Chat**: Ask "What is Master Data Management?"
3. **API Check**: Call `/health` endpoint
4. **MDM Dashboard**: Access `/api/mdm/dashboard`
5. **Feature Test**: Try creating an item via API

## Production Considerations

### Data Persistence
- SQLite cache is in-memory (data lost on restart)
- For persistent data, configure external database
- Oracle EBS provides persistent storage when connected

### Security
- Set strong `SECRET_KEY` in environment variables
- Use HTTPS (Render provides this automatically)
- Validate all input data through AI quality checks
- Monitor API usage and implement rate limiting if needed

### Monitoring
- Use Render's built-in monitoring
- Monitor `/health` endpoint for application status
- Track MDM operation success rates
- Monitor data quality scores and trends

## Support and Maintenance

The application is designed for minimal maintenance:
- Automatic memory management
- Self-healing fallback mechanisms
- Comprehensive error handling
- Built-in data quality monitoring
- Automatic Oracle EBS mock fallback
