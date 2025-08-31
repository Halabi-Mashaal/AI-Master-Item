# Render Deployment Guide - Master Item AI Agent with MDM Guidelines

## 🚀 Quick Deployment Steps

### 1. Connect Repository to Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service" 
3. Connect your GitHub repository: `AI-Master-Item`
4. Choose branch: `main`

### 2. Configure Web Service Settings

**Basic Settings:**
- **Name**: `master-item-ai-agent`
- **Region**: Choose closest to your users
- **Branch**: `main` 
- **Root Directory**: (leave empty)
- **Environment**: `Python 3`
- **Build Command**: 
  ```bash
  pip install --upgrade pip && pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  gunicorn --bind 0.0.0.0:$PORT src.app:app --timeout 120 --workers 1 --max-requests 100
  ```

### 3. Environment Variables (Required)

Add these in Render Dashboard → Service → Environment:

**Required Variables:**
```
USE_LIGHTWEIGHT_NLP=1
MEMORY_OPTIMIZED=1  
DISABLE_HEAVY_MODELS=1
FLASK_ENV=production
```

**Optional AI Provider Variables:**
```
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
AI_PROVIDER=openai
```

**Performance Variables:**
```
WEB_CONCURRENCY=1
MAX_WORKERS=1
```

### 4. Advanced Settings
- **Plan**: Select based on your needs (Start with Free tier)
- **Auto-Deploy**: Yes (deploys automatically on git push)
- **Health Check Path**: `/api/status`

## 📋 Deployment Checklist

### Pre-Deployment ✅
- [x] Oracle EBS dependencies removed
- [x] MDM Guidelines system implemented  
- [x] Heavy ML models disabled for deployment
- [x] Environment variables configured
- [x] Requirements.txt optimized
- [x] Gunicorn configuration set

### Post-Deployment Testing
1. **Health Check**: `GET /api/status`
2. **MDM Validation**: `POST /api/mdm/validate-item`
3. **Guidelines Retrieval**: `GET /api/mdm/guidelines`
4. **Chat Functionality**: `POST /api/chat`

## 🔧 Configuration Files

### requirements.txt
Optimized for Render with lightweight dependencies:
- Flask, Gunicorn for web serving
- OpenAI, Google Generative AI for AI features
- TextBlob, scikit-learn for lightweight NLP
- Pandas, openpyxl for file processing
- **No heavy ML models** (transformers, torch, spacy)

### Environment Configuration
- **Lightweight NLP**: Uses TextBlob instead of transformers
- **Memory Optimized**: Reduced model loading
- **Production Ready**: Gunicorn with optimized workers

## 📊 Expected Performance

### Resource Usage (Render Free Tier Compatible)
- **Memory**: ~200-300MB (vs 2GB+ with heavy models)
- **CPU**: Low to moderate usage
- **Cold Start**: ~10-15 seconds
- **Response Time**: 100-500ms for most endpoints

### Features Available
✅ **MDM Guidelines Validation**: Full Oracle standards compliance  
✅ **Bulk Item Validation**: Excel/CSV processing
✅ **AI Chat**: OpenAI/Gemini integration
✅ **Dashboard**: MDM compliance metrics
✅ **File Analysis**: Document and spreadsheet processing
✅ **Multilingual**: Arabic/English support

## 🚨 Important Notes

### What's Different in Production
1. **No Heavy NLP Models**: Uses lightweight alternatives
2. **No Local Model Loading**: All AI via external APIs
3. **Optimized Memory**: Reduced dependencies
4. **Oracle Independent**: No database connectivity needed

### Monitoring and Debugging
- **Logs**: Available in Render Dashboard → Logs
- **Health Endpoint**: `/api/status` for uptime monitoring
- **Error Handling**: Graceful fallbacks for missing dependencies

## 📞 Support Endpoints

After deployment, test these key endpoints:

### Core Functionality
```bash
# Health check
curl https://your-service.onrender.com/api/status

# MDM validation
curl -X POST https://your-service.onrender.com/api/mdm/validate-item \
  -H "Content-Type: application/json" \
  -d '{"item_number":"TEST001","description":"Test Item"}'

# Get MDM guidelines  
curl https://your-service.onrender.com/api/mdm/guidelines

# Chat with AI
curl -X POST https://your-service.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What are the Oracle MDM guidelines?"}'
```

## 🎯 Success Criteria

Your deployment is successful when:
1. ✅ Health check returns 200 status
2. ✅ MDM validation endpoints work
3. ✅ AI chat responds appropriately  
4. ✅ No Oracle/database errors in logs
5. ✅ Memory usage stays under limits

---

**Next Steps After Deployment:**
1. Test all key functionality
2. Monitor performance and logs
3. Set up custom domain (optional)
4. Configure alerts for downtime
5. Document API endpoints for users
