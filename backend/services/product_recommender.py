from typing import Dict, Any, List

class ProductRecommender:
    """Financial product recommendation engine"""
    
    # Mock financial products database
    PRODUCTS = [
        {
            'id': 'term_loan_1',
            'name': 'Business Term Loan',
            'type': 'Term Loan',
            'provider': 'HDFC Bank',
            'min_amount': 500000,
            'max_amount': 50000000,
            'interest_rate': '10.5% - 14.5%',
            'tenure': '1-7 years',
            'min_credit_score': 60,
            'description': 'Long-term financing for business expansion, equipment purchase, or working capital',
            'eligibility': ['Minimum 2 years in business', 'Positive cash flow', 'Good credit history']
        },
        {
            'id': 'working_capital_1',
            'name': 'Working Capital Loan',
            'type': 'Working Capital',
            'provider': 'ICICI Bank',
            'min_amount': 100000,
            'max_amount': 20000000,
            'interest_rate': '11% - 16%',
            'tenure': '6 months - 3 years',
            'min_credit_score': 50,
            'description': 'Short-term financing for day-to-day operations and inventory management',
            'eligibility': ['Minimum 1 year in business', 'Regular revenue stream']
        },
        {
            'id': 'invoice_financing_1',
            'name': 'Invoice Discounting',
            'type': 'Invoice Financing',
            'provider': 'Axis Bank',
            'min_amount': 50000,
            'max_amount': 10000000,
            'interest_rate': '12% - 18%',
            'tenure': '30-90 days',
            'min_credit_score': 55,
            'description': 'Quick cash against outstanding invoices to improve cash flow',
            'eligibility': ['B2B business model', 'Verified customer invoices']
        },
        {
            'id': 'm  _loan_1',
            'name': 'M   Growth Loan',
            'type': 'M   Loan',
            'provider': 'SBI',
            'min_amount': 250000,
            'max_amount': 30000000,
            'interest_rate': '9.5% - 13.5%',
            'tenure': '1-5 years',
            'min_credit_score': 65,
            'description': 'Government-backed loan for M   sector with attractive interest rates',
            'eligibility': ['M   registration', 'Minimum 3 years in business', 'Strong financials']
        },
        {
            'id': 'overdraft_1',
            'name': 'Cash Credit/Overdraft',
            'type': 'Overdraft',
            'provider': 'Kotak Mahindra Bank',
            'min_amount': 100000,
            'max_amount': 15000000,
            'interest_rate': '10% - 15%',
            'tenure': 'Revolving',
            'min_credit_score': 58,
            'description': 'Flexible credit line for managing short-term cash flow gaps',
            'eligibility': ['Minimum 2 years in business', 'Stable revenue']
        },
        {
            'id': 'equipment_loan_1',
            'name': 'Equipment Financing',
            'type': 'Equipment Loan',
            'provider': 'Bajaj Finserv (NBFC)',
            'min_amount': 200000,
            'max_amount': 25000000,
            'interest_rate': '11.5% - 16.5%',
            'tenure': '1-5 years',
            'min_credit_score': 55,
            'description': 'Financing for purchasing machinery, equipment, or technology',
            'eligibility': ['Equipment invoice/quotation', 'Business profitability']
        },
        {
            'id': 'trade_credit_1',
            'name': 'Trade Credit Line',
            'type': 'Trade Finance',
            'provider': 'IDFC First Bank',
            'min_amount': 500000,
            'max_amount': 40000000,
            'interest_rate': '9% - 13%',
            'tenure': '3-12 months',
            'min_credit_score': 70,
            'description': 'Credit facility for import/export businesses and trade transactions',
            'eligibility': ['Import/export license', 'Trade documentation', 'Strong credit profile']
        },
        {
            'id': 'unsecured_loan_1',
            'name': 'Unsecured Business Loan',
            'type': 'Unsecured Loan',
            'provider': 'Tata Capital (NBFC)',
            'min_amount': 100000,
            'max_amount': 7500000,
            'interest_rate': '14% - 20%',
            'tenure': '1-4 years',
            'min_credit_score': 62,
            'description': 'Quick loan without collateral for immediate business needs',
            'eligibility': ['Minimum 1 year in business', 'ITR for last 2 years']
        }
    ]
    
    @staticmethod
    def recommend_products(
        health_score: int,
        metrics: Dict[str, Dict[str, float]],
        financial_data: Dict[str, float],
        industry: str,
        business_needs: List[str] = None,
        language: str = 'en'
    ) -> List[Dict[str, Any]]:
        """
        Recommend suitable financial products
        
        Args:
            health_score: Financial health score (0-100)
            metrics: Calculated financial metrics
            financial_data: Raw financial data
            industry: Business industry
            business_needs: List of specific needs (optional)
            
        Returns:
            List of recommended products with eligibility status
        """
        recommendations = []
        
        # Determine business needs if not provided
        if not business_needs:
            business_needs = ProductRecommender._identify_needs(metrics, financial_data)
        
        for product in ProductRecommender.PRODUCTS:
            # Check eligibility
            eligible = health_score >= product['min_credit_score']
            
            # Calculate match score
            match_score = ProductRecommender._calculate_match_score(
                product,
                business_needs,
                metrics,
                financial_data
            )
            
            if match_score > 0:
                recommendations.append({
                    **product,
                    'eligible': eligible,
                    'match_score': match_score,
                    'reason': ProductRecommender._get_recommendation_reason(
                        product,
                        business_needs,
                        metrics
                    )
                })
        
        # Sort by match score and eligibility
        recommendations.sort(key=lambda x: (x['eligible'], x['match_score']), reverse=True)
        
        return recommendations[:5]  # Return top 5
    
    @staticmethod
    def _identify_needs(
        metrics: Dict[str, Dict[str, float]],
        financial_data: Dict[str, float]
    ) -> List[str]:
        """Identify business financial needs based on metrics"""
        needs = []
        
        # Check liquidity
        if metrics['liquidity']['current_ratio'] < 1.2:
            needs.append('working_capital')
            needs.append('cash_flow')
        
        # Check cash conversion cycle
        if metrics['working_capital']['cash_conversion_cycle'] > 60:
            needs.append('invoice_financing')
        
        # Check profitability for growth
        if metrics['profitability']['net_profit_margin'] > 10:
            needs.append('expansion')
            needs.append('equipment')
        
        # Check leverage
        if metrics['leverage']['debt_to_equity'] < 0.5:
            needs.append('growth_capital')
        
        return needs if needs else ['general_purpose']
    
    @staticmethod
    def _calculate_match_score(
        product: Dict[str, Any],
        needs: List[str],
        metrics: Dict[str, Dict[str, float]],
        financial_data: Dict[str, float]
    ) -> int:
        """Calculate how well a product matches business needs"""
        score = 0
        
        product_type = product['type'].lower()
        
        # Match product type to needs
        if 'working_capital' in needs and 'working capital' in product_type:
            score += 40
        if 'cash_flow' in needs and product_type in ['working capital', 'overdraft', 'invoice financing']:
            score += 35
        if 'invoice_financing' in needs and 'invoice' in product_type:
            score += 45
        if 'expansion' in needs and 'term loan' in product_type:
            score += 40
        if 'equipment' in needs and 'equipment' in product_type:
            score += 45
        if 'growth_capital' in needs and product_type in ['term loan', 'm   loan']:
            score += 35
        
        # General purpose match
        if 'general_purpose' in needs:
            score += 20
        
        # Bonus for government-backed loans
        if 'm  ' in product_type:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _get_recommendation_reason(
        product: Dict[str, Any],
        needs: List[str],
        metrics: Dict[str, Dict[str, float]]
    ) -> str:
        """Generate reason for recommendation"""
        product_type = product['type'].lower()
        
        if 'working_capital' in needs and 'working capital' in product_type:
            return "Recommended to improve working capital and liquidity position"
        elif 'invoice_financing' in needs and 'invoice' in product_type:
            return "Ideal for reducing cash conversion cycle and improving cash flow"
        elif 'expansion' in needs and 'term loan' in product_type:
            return "Suitable for business expansion with strong profitability"
        elif 'equipment' in needs and 'equipment' in product_type:
            return "Perfect for acquiring new equipment or technology"
        else:
            return "Matches your business profile and financial needs"

product_recommender = ProductRecommender()
