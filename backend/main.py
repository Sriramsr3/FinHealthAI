from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
import logging
from typing import Optional

# Import configuration
from config.settings import settings

# Import database
from database import get_db, init_db, BusinessProfile as DBBusinessProfile, FinancialStatement as DBFinancialStatement, AnalysisResult as DBAnalysisResult

# Import models/schemas
from models.schemas import (
    AnalysisRequest,
    HealthAssessment,
    ForecastRequest,
    BenchmarkRequest,
    TranslationRequest,
    ErrorResponse
)

# Import services
from services import (
    financial_analyzer,
    openai_service,
    document_parser,
    industry_benchmark,
    product_recommender,
    tax_compliance,
    cash_flow_forecaster,
    translation_service
)

# Import security
from security import limiter, validate_input

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered financial health assessment platform for   s",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting
app.state.limiter = limiter

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    try:
        init_db()
        logger.info("Database initialized successfully")
        logger.info(f"OpenAI integration: {'Enabled' if settings.OPENAI_ENABLED else 'Disabled (using rule-based fallback)'}")
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "status": "online",
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "openai_enabled": settings.OPENAI_ENABLED
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2026-02-04T12:00:00Z"}

@app.post("/analyze", response_model=HealthAssessment)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def analyze_finances(
    request: Request,
    analysis_request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Comprehensive financial analysis endpoint
    
    Analyzes financial statements and provides:
    - Health score and risk assessment
    - AI-powered insights and recommendations
    - Industry benchmarking
    - Financial product recommendations
    - Tax compliance check
    - Cash flow forecast
    """
    try:
        # Extract data
        business_profile = analysis_request.business_profile
        financial_data = analysis_request.financial_statement.dict()
        language = analysis_request.language
        
        # Validate business name
        validate_input(business_profile.name, max_length=255)
        
        # Calculate comprehensive metrics
        metrics = financial_analyzer.calculate_all_metrics(financial_data)
        
        # Calculate health score
        health_score = financial_analyzer.calculate_health_score(
            metrics,
            business_profile.industry.value
        )
        
        # Determine risk level
        risk_level = financial_analyzer.determine_risk_level(health_score, metrics)
        
        # Generate AI insights
        insights = openai_service.generate_insights(
            financial_data,
            metrics,
            business_profile.industry.value,
            business_profile.business_type.value,
            language=language
        )
        
        # Generate recommendations
        recommendations = openai_service.generate_recommendations(
            insights,
            metrics,
            risk_level,
            business_profile.industry.value,
            language=language
        )
        
        # Industry benchmark comparison
        benchmark_comparison = industry_benchmark.get_benchmark_comparison(
            metrics,
            business_profile.industry.value,
            language=language
        )
        
        # Product recommendations
        product_recs = product_recommender.recommend_products(
            health_score,
            metrics,
            financial_data,
            business_profile.industry.value,
            language=language
        )
        
        # Tax compliance check
        tax_status = tax_compliance.check_compliance(
            financial_data,
            business_profile.industry.value,
            business_profile.business_type.value,
            language=language
        )
        
        # Cash flow forecast
        forecast = cash_flow_forecaster.forecast_cash_flow(
            financial_data,
            metrics,
            business_profile.industry.value,
            months=12,
            language=language
        )
        
        # Save to database
        try:
            # Create or get business profile
            db_business = DBBusinessProfile(
                name=business_profile.name,
                business_type=business_profile.business_type,
                industry=business_profile.industry,
                size=business_profile.size,
                location=business_profile.location,
                years_in_operation=business_profile.years_in_operation
            )
            db.add(db_business)
            db.commit()
            db.refresh(db_business)
            
            # Save financial statement
            db_statement = DBFinancialStatement(
                business_id=db_business.id,
                **financial_data
            )
            db.add(db_statement)
            db.commit()
            db.refresh(db_statement)
            
            # Save analysis result
            db_analysis = DBAnalysisResult(
                business_id=db_business.id,
                statement_id=db_statement.id,
                health_score=health_score,
                creditworthiness_score=health_score,  # Same for now
                risk_level=risk_level,
                insights=insights,
                recommendations=recommendations,
                metrics=metrics,
                forecast_data=forecast,
                benchmark_data=benchmark_comparison,
                product_recommendations=product_recs
            )
            db.add(db_analysis)
            db.commit()
            
            logger.info(f"Analysis saved for business: {business_profile.name}")
        except Exception as db_error:
            logger.error(f"Database error: {db_error}")
            # Continue even if database save fails
        
        # Prepare response
        response = HealthAssessment(
            health_score=health_score,
            creditworthiness_score=health_score,
            risk_level=risk_level,
            insights=insights,
            recommendations=recommendations,
            metrics=metrics,
            benchmark_comparison=benchmark_comparison,
            product_recommendations=product_recs,
            tax_compliance=tax_status,
            cash_flow_forecast=forecast
        )
        
        # Translate if needed
        if language != 'en':
            response_dict = response.dict()
            response_dict['risk_level'] = translation_service.translate(risk_level, language)
            # Note: Full translation of insights/recommendations would require AI translation
            return response_dict
        
        return response
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/upload", response_model=HealthAssessment)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def upload_financial_document(
    request: Request,
    file: UploadFile = File(...),
    business_name: str = "Unknown Business",
    business_type: str = "private_limited",
    industry: str = "services",
    language: str = "en",
    db: Session = Depends(get_db)
):
    """
    Upload and analyze financial document (CSV, XLSX, PDF)
    """
    try:
        # Validate file size
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Reset file pointer
        await file.seek(0)
        
        # Parse document
        financial_data = await document_parser.parse_file(file)
        
        # Create analysis request
        from database.models import BusinessType, Industry
        
        analysis_request = AnalysisRequest(
            business_profile={
                "name": business_name,
                "business_type": BusinessType(business_type),
                "industry": Industry(industry)
            },
            financial_statement=financial_data,
            language=language
        )
        
        # Reuse analyze endpoint logic
        return await analyze_finances(request, analysis_request, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/forecast")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_cash_flow_forecast(request: Request, forecast_request: ForecastRequest):
    """Get cash flow forecast"""
    try:
        financial_data = forecast_request.financial_statement.dict()
        metrics = financial_analyzer.calculate_all_metrics(financial_data)
        
        forecast = cash_flow_forecaster.forecast_cash_flow(
            financial_data,
            metrics,
            forecast_request.industry.value,
            forecast_request.months
        )
        
        return forecast
    except Exception as e:
        logger.error(f"Forecast error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecast failed: {str(e)}")

@app.post("/benchmark")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_industry_benchmark(request: Request, benchmark_request: BenchmarkRequest):
    """Get industry benchmark comparison"""
    try:
        comparison = industry_benchmark.get_benchmark_comparison(
            benchmark_request.metrics,
            benchmark_request.industry.value
        )
        return comparison
    except Exception as e:
        logger.error(f"Benchmark error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")

@app.post("/translate")
async def translate_content(translation_request: TranslationRequest):
    """Translate content to specified language"""
    try:
        translated = translation_service.translate_dict(
            translation_request.data,
            translation_request.language
        )
        return translated
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/translations/{language}")
async def get_translations(language: str):
    """Get all UI translations for a language"""
    try:
        translations = translation_service.get_all_translations(language)
        return translations
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Language not found: {language}")

# Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": str(exc.status_code)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
