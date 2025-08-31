#!/usr/bin/env python3
"""
Production startup script for Render deployment
Optimized for lightweight deployment without heavy ML models
"""
import os
import sys
import logging

# Set production environment variables
os.environ.setdefault('USE_LIGHTWEIGHT_NLP', '1')
os.environ.setdefault('MEMORY_OPTIMIZED', '1')
os.environ.setdefault('DISABLE_HEAVY_MODELS', '1')
os.environ.setdefault('FLASK_ENV', 'production')

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def verify_deployment_readiness():
    """Verify the application is ready for production deployment"""
    logger.info("Verifying deployment readiness...")
    
    try:
        # Check core imports
        logger.info("Testing core application imports...")
        sys.path.insert(0, 'src')
        
        from app import app
        logger.info("✅ Flask application imported successfully")
        
        from mdm_guidelines import validate_item_data, get_mdm_guidelines
        logger.info("✅ MDM Guidelines system available")
        
        # Test MDM functionality
        test_item = {"item_number": "TEST001", "description": "Test Item"}
        result = validate_item_data(test_item)
        logger.info(f"✅ MDM validation working - Score: {result.score}%")
        
        # Check environment configuration
        if os.environ.get('USE_LIGHTWEIGHT_NLP') == '1':
            logger.info("✅ Lightweight NLP mode enabled")
        
        if os.environ.get('MEMORY_OPTIMIZED') == '1':
            logger.info("✅ Memory optimization enabled")
            
        logger.info("🎉 Application ready for production!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Deployment readiness check failed: {e}")
        return False

def start_application():
    """Start the Flask application"""
    logger.info("Starting Master Item AI Agent with MDM Guidelines...")
    
    # Import after path setup
    sys.path.insert(0, 'src')
    from app import app
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 8000))
    
    logger.info(f"Starting application on port {port}")
    logger.info("Features available:")
    logger.info("  ✅ Oracle MDM Guidelines Validation")
    logger.info("  ✅ Bulk Item Processing")
    logger.info("  ✅ AI-Powered Chat (OpenAI/Gemini)")
    logger.info("  ✅ File Analysis and Processing")
    logger.info("  ✅ Multilingual Support (Arabic/English)")
    logger.info("  ❌ Oracle EBS Integration (Removed)")
    
    # Start Flask development server if running directly
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=port, debug=False)
    
    return app

if __name__ == "__main__":
    # Verify deployment readiness
    if not verify_deployment_readiness():
        sys.exit(1)
    
    # Start the application
    app = start_application()
else:
    # For Gunicorn deployment
    logger.info("Loading application for Gunicorn...")
    sys.path.insert(0, 'src')
    from app import app
