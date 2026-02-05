from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FinancialAnalyzer:
    """Advanced financial analysis service with comprehensive metrics"""
    
    @staticmethod
    def calculate_all_metrics(data: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate comprehensive financial metrics
        
        Args:
            data: Dictionary with financial statement data
            
        Returns:
            Dictionary with calculated metrics organized by category
        """
        metrics = {
            'liquidity': FinancialAnalyzer._calculate_liquidity_ratios(data),
            'profitability': FinancialAnalyzer._calculate_profitability_ratios(data),
            'leverage': FinancialAnalyzer._calculate_leverage_ratios(data),
            'efficiency': FinancialAnalyzer._calculate_efficiency_ratios(data),
            'working_capital': FinancialAnalyzer._calculate_working_capital_metrics(data)
        }
        
        return metrics
    
    @staticmethod
    def _calculate_liquidity_ratios(data: Dict[str, float]) -> Dict[str, float]:
        """Calculate liquidity ratios"""
        current_assets = data.get('current_assets', 0)
        current_liabilities = data.get('current_liabilities', 1)  # Avoid division by zero
        inventory = data.get('inventory', 0)
        cash = data.get('cash', 0)
        
        return {
            'current_ratio': round(current_assets / current_liabilities if current_liabilities > 0 else 0, 2),
            'quick_ratio': round((current_assets - inventory) / current_liabilities if current_liabilities > 0 else 0, 2),
            'cash_ratio': round(cash / current_liabilities if current_liabilities > 0 else 0, 2)
        }
    
    @staticmethod
    def _calculate_profitability_ratios(data: Dict[str, float]) -> Dict[str, float]:
        """Calculate profitability ratios"""
        revenue = data.get('revenue', 1)
        cogs = data.get('cogs', 0)
        operating_expenses = data.get('operating_expenses', 0)
        net_income = data.get('net_income', 0)
        total_assets = data.get('total_assets', 1)
        equity = data.get('total_assets', 0) - data.get('total_liabilities', 0)
        
        gross_profit = revenue - cogs
        operating_income = gross_profit - operating_expenses
        
        return {
            'gross_profit_margin': round((gross_profit / revenue * 100) if revenue > 0 else 0, 2),
            'operating_profit_margin': round((operating_income / revenue * 100) if revenue > 0 else 0, 2),
            'net_profit_margin': round((net_income / revenue * 100) if revenue > 0 else 0, 2),
            'return_on_assets': round((net_income / total_assets * 100) if total_assets > 0 else 0, 2),
            'return_on_equity': round((net_income / equity * 100) if equity > 0 else 0, 2)
        }
    
    @staticmethod
    def _calculate_leverage_ratios(data: Dict[str, float]) -> Dict[str, float]:
        """Calculate leverage/solvency ratios"""
        total_assets = data.get('total_assets', 1)
        total_liabilities = data.get('total_liabilities', 0)
        equity = total_assets - total_liabilities
        net_income = data.get('net_income', 0)
        
        # Estimate interest expense (simplified)
        interest_expense = total_liabilities * 0.08  # Assume 8% average interest rate
        ebit = net_income + interest_expense
        
        return {
            'debt_to_equity': round(total_liabilities / equity if equity > 0 else 0, 2),
            'debt_to_assets': round(total_liabilities / total_assets if total_assets > 0 else 0, 2),
            'equity_ratio': round(equity / total_assets if total_assets > 0 else 0, 2),
            'interest_coverage': round(ebit / interest_expense if interest_expense > 0 else 0, 2)
        }
    
    @staticmethod
    def _calculate_efficiency_ratios(data: Dict[str, float]) -> Dict[str, float]:
        """Calculate efficiency/activity ratios"""
        revenue = data.get('revenue', 1)
        total_assets = data.get('total_assets', 1)
        inventory = data.get('inventory', 1)
        receivables = data.get('receivables', 1)
        cogs = data.get('cogs', 0)
        
        return {
            'asset_turnover': round(revenue / total_assets if total_assets > 0 else 0, 2),
            'inventory_turnover': round(cogs / inventory if inventory > 0 else 0, 2),
            'receivables_turnover': round(revenue / receivables if receivables > 0 else 0, 2),
            'days_sales_outstanding': round((receivables / revenue * 365) if revenue > 0 else 0, 1),
            'days_inventory_outstanding': round((inventory / cogs * 365) if cogs > 0 else 0, 1)
        }
    
    @staticmethod
    def _calculate_working_capital_metrics(data: Dict[str, float]) -> Dict[str, float]:
        """Calculate working capital metrics"""
        current_assets = data.get('current_assets', 0)
        current_liabilities = data.get('current_liabilities', 0)
        inventory = data.get('inventory', 0)
        receivables = data.get('receivables', 0)
        payables = data.get('payables', 1)
        revenue = data.get('revenue', 1)
        cogs = data.get('cogs', 0)
        
        working_capital = current_assets - current_liabilities
        
        # Cash Conversion Cycle
        dso = (receivables / revenue * 365) if revenue > 0 else 0
        dio = (inventory / cogs * 365) if cogs > 0 else 0
        dpo = (payables / cogs * 365) if cogs > 0 else 0
        ccc = dso + dio - dpo
        
        return {
            'working_capital': round(working_capital, 2),
            'working_capital_ratio': round(working_capital / revenue if revenue > 0 else 0, 2),
            'cash_conversion_cycle': round(ccc, 1)
        }
    
    @staticmethod
    def calculate_health_score(metrics: Dict[str, Dict[str, float]], industry: str = "services") -> int:
        """
        Calculate overall financial health score (0-100)
        
        Args:
            metrics: Dictionary of calculated metrics
            industry: Industry type for benchmarking
            
        Returns:
            Health score (0-100)
        """
        score = 70  # Base score
        
        # Liquidity scoring (20 points max)
        current_ratio = metrics['liquidity']['current_ratio']
        if current_ratio >= 2.0:
            score += 20
        elif current_ratio >= 1.5:
            score += 15
        elif current_ratio >= 1.0:
            score += 10
        elif current_ratio >= 0.5:
            score += 5
        else:
            score -= 10
        
        # Profitability scoring (30 points max)
        npm = metrics['profitability']['net_profit_margin']
        if npm >= 15:
            score += 30
        elif npm >= 10:
            score += 20
        elif npm >= 5:
            score += 10
        elif npm >= 0:
            score += 5
        else:
            score -= 20
        
        # Leverage scoring (20 points max)
        debt_to_equity = metrics['leverage']['debt_to_equity']
        equity_ratio = metrics['leverage']['equity_ratio']
        
        if equity_ratio <= 0:
            score -= 30  # Heavy penalty for zero/negative equity
        elif debt_to_equity <= 0.5:
            score += 20
        elif debt_to_equity <= 1.0:
            score += 15
        elif debt_to_equity <= 2.0:
            score += 5
        else:
            score -= 10
        
        # Efficiency scoring (15 points max)
        asset_turnover = metrics['efficiency']['asset_turnover']
        if asset_turnover >= 2.0:
            score += 15
        elif asset_turnover >= 1.0:
            score += 10
        elif asset_turnover >= 0.5:
            score += 5
        
        # Working capital scoring (15 points max)
        wc = metrics['working_capital']['working_capital']
        if wc > 0:
            score += 15
        elif wc > -100000:
            score += 5
        else:
            score -= 10
        
        # Ensure score is within 0-100
        return max(0, min(100, score))
    
    @staticmethod
    def determine_risk_level(score: int, metrics: Dict[str, Dict[str, float]]) -> str:
        """
        Determine risk level based on health score and metrics
        
        Args:
            score: Health score
            metrics: Financial metrics
            
        Returns:
            Risk level: "Low", "Moderate", "High", or "Critical"
        """
        # Score-based risk levels (primary determinant)
        if score >= 80:
            main_risk = "Low"
        elif score >= 60:
            main_risk = "Moderate"
        elif score >= 40:
            main_risk = "High"
        else:
            main_risk = "Critical"
            
        # Check for absolute critical conditions that might override a moderate score
        equity = metrics['leverage']['equity_ratio']
        current_ratio = metrics['liquidity']['current_ratio']
        npm = metrics['profitability']['net_profit_margin']
        
        if (equity <= 0 or current_ratio < 0.3 or npm < -50) and main_risk != "Critical":
            # If there's a fatal flaw but the score is otherwise high, don't say 'Low'
            if main_risk == "Low":
                return "Moderate" # At least moderate risk if there's a fatal flaw
            return main_risk
            
        return main_risk

financial_analyzer = FinancialAnalyzer()
