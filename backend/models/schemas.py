from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from database.models import BusinessType, Industry, RiskLevel

class FinancialStatement(BaseModel):
    """Financial statement data model"""
    revenue: float = Field(..., description="Total revenue", ge=0)
    cogs: float = Field(0, description="Cost of goods sold", ge=0)
    operating_expenses: float = Field(0, description="Operating expenses", ge=0)
    net_income: float = Field(..., description="Net income (can be negative)")
    total_assets: float = Field(..., description="Total assets", ge=0)
    current_assets: float = Field(0, description="Current assets", ge=0)
    total_liabilities: float = Field(..., description="Total liabilities", ge=0)
    current_liabilities: float = Field(0, description="Current liabilities", ge=0)
    inventory: float = Field(0, description="Inventory", ge=0)
    receivables: float = Field(0, description="Accounts receivable", ge=0)
    payables: float = Field(0, description="Accounts payable", ge=0)
    cash: float = Field(0, description="Cash and equivalents", ge=0)

class BusinessProfile(BaseModel):
    """Business profile information"""
    name: str = Field(..., description="Business name")
    business_type: BusinessType = Field(..., description="Type of business entity")
    industry: Industry = Field(..., description="Industry sector")
    size: Optional[str] = Field("Medium", description="Business size: Small, Medium, Large")
    location: Optional[str] = Field(None, description="Business location")
    years_in_operation: Optional[int] = Field(None, description="Years in business", ge=0)

class AnalysisRequest(BaseModel):
    """Complete analysis request with business profile and financial data"""
    business_profile: BusinessProfile
    financial_statement: FinancialStatement
    language: Optional[str] = Field("en", description="Response language: en, hi, ta, te")

class MetricsResponse(BaseModel):
    """Financial metrics response"""
    liquidity: Dict[str, float]
    profitability: Dict[str, float]
    leverage: Dict[str, float]
    efficiency: Dict[str, float]
    working_capital: Dict[str, float]

class HealthAssessment(BaseModel
):
    """Comprehensive health asses  nt response"""
    health_score: int = Field(..., description="Financial health score (0-100)")
    creditworthiness_score: int = Field(..., description="Creditworthiness score (0-100)")
    risk_level: str = Field(..., description="Risk level: Low, Moderate, High, Critical")
    insights: List[str] = Field(..., description="AI-generated insights")
    recommendations: List[str] = Field(..., description="Strategic recommendations")
    metrics: MetricsResponse = Field(..., description="Calculated financial metrics")
    benchmark_comparison: Optional[Dict[str, Any]] = Field(None, description="Industry benchmark data")
    product_recommendations: Optional[List[Dict[str, Any]]] = Field(None, description="Recommended financial products")
    tax_compliance: Optional[Dict[str, Any]] = Field(None, description="Tax compliance status")
    cash_flow_forecast: Optional[Dict[str, Any]] = Field(None, description="Cash flow projections")

class ForecastRequest(BaseModel):
    """Cash flow forecast request"""
    financial_statement: FinancialStatement
    industry: Industry
    months: int = Field(12, description="Number of months to forecast", ge=1, le=36)

class BenchmarkRequest(BaseModel):
    """Industry benchmark request"""
    metrics: Dict[str, Dict[str, float]]
    industry: Industry

class TranslationRequest(BaseModel):
    """Translation request"""
    data: Dict[str, Any]
    language: str = Field(..., description="Target language: en, hi, ta, te")

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    error_code: Optional[str] = None
