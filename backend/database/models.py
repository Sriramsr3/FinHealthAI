from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database.connection import Base

class BusinessType(str, enum.Enum):
    SOLE_PROPRIETORSHIP = "sole_proprietorship"
    PARTNERSHIP = "partnership"
    PRIVATE_LIMITED = "private_limited"
    PUBLIC_LIMITED = "public_limited"
    LLP = "llp"

class Industry(str, enum.Enum):
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    AGRICULTURE = "agriculture"
    SERVICES = "services"
    LOGISTICS = "logistics"
    ECOMMERCE = "ecommerce"
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    HOSPITALITY = "hospitality"
    CONSTRUCTION = "construction"

class RiskLevel(str, enum.Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

class BusinessProfile(Base):
    __tablename__ = "business_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    business_type = Column(Enum(BusinessType), nullable=False)
    industry = Column(Enum(Industry), nullable=False)
    size = Column(String(50))  # Small, Medium, Large
    location = Column(String(255))
    years_in_operation = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    financial_statements = relationship("FinancialStatement", back_populates="business")
    analysis_results = relationship("AnalysisResult", back_populates="business")

class FinancialStatement(Base):
    __tablename__ = "financial_statements"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_profiles.id"), nullable=False)
    period = Column(String(50))  # e.g., "2024-Q1", "2024-Annual"
    
    # Income Statement
    revenue = Column(Float, nullable=False)
    cogs = Column(Float, default=0)
    operating_expenses = Column(Float, default=0)
    net_income = Column(Float, nullable=False)
    
    # Balance Sheet
    total_assets = Column(Float, nullable=False)
    current_assets = Column(Float, default=0)
    total_liabilities = Column(Float, nullable=False)
    current_liabilities = Column(Float, default=0)
    
    # Additional Metrics
    inventory = Column(Float, default=0)
    receivables = Column(Float, default=0)
    payables = Column(Float, default=0)
    cash = Column(Float, default=0)
    
    # Encrypted sensitive data (JSON)
    encrypted_data = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("BusinessProfile", back_populates="financial_statements")
    analysis_results = relationship("AnalysisResult", back_populates="statement")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business_profiles.id"), nullable=False)
    statement_id = Column(Integer, ForeignKey("financial_statements.id"), nullable=False)
    
    # Scores and Risk
    health_score = Column(Integer, nullable=False)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    creditworthiness_score = Column(Integer)
    
    # Analysis Results (JSON)
    insights = Column(JSON)
    recommendations = Column(JSON)
    metrics = Column(JSON)
    forecast_data = Column(JSON, nullable=True)
    benchmark_data = Column(JSON, nullable=True)
    product_recommendations = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("BusinessProfile", back_populates="analysis_results")
    statement = relationship("FinancialStatement", back_populates="analysis_results")

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    business_id = Column(Integer, ForeignKey("business_profiles.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Integer, default=1)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=True)
    business_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
