from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta

class CashFlowForecaster:
    """Financial forecasting and cash flow projection service"""
    
    @staticmethod
    def forecast_cash_flow(
        financial_data: Dict[str, float],
        metrics: Dict[str, Dict[str, float]],
        industry: str,
        months: int = 12,
        language: str = 'en'
    ) -> Dict[str, Any]:
        """
        Generate cash flow forecast
        
        Args:
            financial_data: Current financial data
            metrics: Calculated metrics
            industry: Business industry
            months: Number of months to forecast
            
        Returns:
            Dictionary with forecast data
        """
        revenue = financial_data.get('revenue', 0)
        net_income = financial_data.get('net_income', 0)
        current_assets = financial_data.get('current_assets', 0)
        current_liabilities = financial_data.get('current_liabilities', 0)
        
        # Calculate monthly averages
        monthly_revenue = revenue / 12
        monthly_net_income = net_income / 12
        
        # Generate forecast
        forecast = {
            'forecast_period': f"{months} months",
            'monthly_projections': CashFlowForecaster._generate_monthly_projections(
                monthly_revenue,
                monthly_net_income,
                industry,
                months
            ),
            'summary': {},
            'working_capital_recommendations': []
        }
        
        # Calculate summary
        total_projected_revenue = sum([m['revenue'] for m in forecast['monthly_projections']])
        total_projected_income = sum([m['net_income'] for m in forecast['monthly_projections']])
        
        forecast['summary'] = {
            'total_projected_revenue': round(total_projected_revenue, 2),
            'total_projected_net_income': round(total_projected_income, 2),
            'average_monthly_revenue': round(total_projected_revenue / months, 2),
            'average_monthly_net_income': round(total_projected_income / months, 2),
            'growth_rate': CashFlowForecaster._calculate_growth_rate(industry)
        }
        
        # Working capital recommendations
        forecast['working_capital_recommendations'] = CashFlowForecaster._generate_wc_recommendations(
            metrics,
            forecast['monthly_projections']
        )
        
        return forecast
    
    @staticmethod
    def _generate_monthly_projections(
        base_monthly_revenue: float,
        base_monthly_income: float,
        industry: str,
        months: int
    ) -> List[Dict[str, Any]]:
        """Generate month-by-month projections"""
        
        # Industry growth rates and seasonality
        growth_rates = {
            'manufacturing': 0.08,  # 8% annual
            'retail': 0.12,
            'services': 0.10,
            'technology': 0.15,
            'agriculture': 0.06,
            'ecommerce': 0.18,
            'logistics': 0.10,
            'healthcare': 0.09,
            'hospitality': 0.11,
            'construction': 0.07
        }
        
        annual_growth = growth_rates.get(industry.lower(), 0.10)
        monthly_growth = annual_growth / 12
        
        # Seasonality factors (simplified)
        seasonality = CashFlowForecaster._get_seasonality_factors(industry, months)
        
        projections = []
        current_date = datetime.now()
        
        for i in range(months):
            month_date = current_date + timedelta(days=30 * i)
            
            # Apply growth and seasonality
            revenue = base_monthly_revenue * (1 + monthly_growth * i) * seasonality[i]
            net_income = base_monthly_income * (1 + monthly_growth * i) * seasonality[i]
            
            # Estimate cash flow components
            operating_cash_flow = net_income * 1.2  # Add back non-cash expenses
            investing_cash_flow = -revenue * 0.05  # Assume 5% reinvestment
            financing_cash_flow = revenue * 0.02  # Assume some debt servicing
            
            net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
            
            projections.append({
                'month': month_date.strftime('%b %Y'),
                'revenue': round(revenue, 2),
                'net_income': round(net_income, 2),
                'operating_cash_flow': round(operating_cash_flow, 2),
                'investing_cash_flow': round(investing_cash_flow, 2),
                'financing_cash_flow': round(financing_cash_flow, 2),
                'net_cash_flow': round(net_cash_flow, 2),
                'cumulative_cash': round(sum([p.get('net_cash_flow', 0) for p in projections]) + net_cash_flow, 2)
            })
        
        return projections
    
    @staticmethod
    def _get_seasonality_factors(industry: str, months: int) -> List[float]:
        """Get seasonality adjustment factors"""
        
        # Simplified seasonality patterns
        patterns = {
            'retail': [0.9, 0.85, 0.95, 1.0, 1.05, 1.1, 1.15, 1.1, 1.05, 1.1, 1.2, 1.3],  # Peak in holidays
            'agriculture': [0.8, 0.85, 0.9, 1.1, 1.2, 1.15, 1.1, 1.05, 1.0, 1.1, 1.15, 0.9],  # Harvest seasons
            'hospitality': [0.85, 0.9, 0.95, 1.05, 1.1, 1.15, 1.2, 1.15, 1.05, 1.0, 0.95, 1.1],  # Tourism peaks
            'default': [1.0] * 12  # No seasonality
        }
        
        pattern = patterns.get(industry.lower(), patterns['default'])
        
        # Repeat pattern for multiple years if needed
        full_pattern = (pattern * ((months // 12) + 1))[:months]
        
        return full_pattern
    
    @staticmethod
    def _calculate_growth_rate(industry: str) -> str:
        """Get expected annual growth rate for industry"""
        rates = {
            'manufacturing': '8%',
            'retail': '12%',
            'services': '10%',
            'technology': '15%',
            'agriculture': '6%',
            'ecommerce': '18%',
            'logistics': '10%',
            'healthcare': '9%',
            'hospitality': '11%',
            'construction': '7%'
        }
        return rates.get(industry.lower(), '10%')
    
    @staticmethod
    def _generate_wc_recommendations(
        metrics: Dict[str, Dict[str, float]],
        projections: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate working capital optimization recommendations"""
        recommendations = []
        
        # Check cash conversion cycle
        ccc = metrics['working_capital']['cash_conversion_cycle']
        if ccc > 60:
            recommendations.append(
                f"Reduce cash conversion cycle from {ccc:.0f} days to below 60 days by "
                "optimizing inventory turnover and accelerating collections"
            )
        
        # Check for negative cash flow months
        negative_months = [p for p in projections if p['net_cash_flow'] < 0]
        if negative_months:
            recommendations.append(
                f"Prepare for {len(negative_months)} months with negative cash flow. "
                "Consider arranging a working capital line of credit"
            )
        
        # Check working capital ratio
        wc_ratio = metrics['working_capital']['working_capital_ratio']
        if wc_ratio < 0.1:
            recommendations.append(
                "Increase working capital buffer to at least 10% of revenue for operational stability"
            )
        
        # General recommendations
        recommendations.append(
            "Maintain a cash reserve equal to 3-6 months of operating expenses for emergencies"
        )
        
        recommendations.append(
            "Implement automated invoicing and payment reminders to reduce DSO by 15-20%"
        )
        
        return recommendations

cash_flow_forecaster = CashFlowForecaster()
