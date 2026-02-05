from typing import Dict, Any, List
from database.models import Industry

class IndustryBenchmark:
    """Industry benchmarking service with standard metrics"""
    
    # Industry benchmark data (typical ranges for healthy businesses)
    BENCHMARKS = {
        Industry.MANUFACTURING: {
            'current_ratio': {'excellent': 2.0, 'good': 1.5, 'average': 1.2, 'poor': 0.8},
            'quick_ratio': {'excellent': 1.5, 'good': 1.0, 'average': 0.8, 'poor': 0.5},
            'net_profit_margin': {'excellent': 15.0, 'good': 10.0, 'average': 5.0, 'poor': 2.0},
            'debt_to_equity': {'excellent': 0.5, 'good': 1.0, 'average': 1.5, 'poor': 2.5},
            'asset_turnover': {'excellent': 2.0, 'good': 1.5, 'average': 1.0, 'poor': 0.5},
            'return_on_equity': {'excellent': 20.0, 'good': 15.0, 'average': 10.0, 'poor': 5.0}
        },
        Industry.RETAIL: {
            'current_ratio': {'excellent': 2.5, 'good': 2.0, 'average': 1.5, 'poor': 1.0},
            'quick_ratio': {'excellent': 1.0, 'good': 0.8, 'average': 0.5, 'poor': 0.3},
            'net_profit_margin': {'excellent': 10.0, 'good': 6.0, 'average': 3.0, 'poor': 1.0},
            'debt_to_equity': {'excellent': 0.3, 'good': 0.7, 'average': 1.2, 'poor': 2.0},
            'asset_turnover': {'excellent': 3.0, 'good': 2.5, 'average': 2.0, 'poor': 1.0},
            'return_on_equity': {'excellent': 25.0, 'good': 18.0, 'average': 12.0, 'poor': 6.0}
        },
        Industry.SERVICES: {
            'current_ratio': {'excellent': 2.0, 'good': 1.5, 'average': 1.2, 'poor': 0.9},
            'quick_ratio': {'excellent': 1.8, 'good': 1.3, 'average': 1.0, 'poor': 0.7},
            'net_profit_margin': {'excellent': 20.0, 'good': 15.0, 'average': 10.0, 'poor': 5.0},
            'debt_to_equity': {'excellent': 0.4, 'good': 0.8, 'average': 1.3, 'poor': 2.0},
            'asset_turnover': {'excellent': 2.5, 'good': 2.0, 'average': 1.5, 'poor': 0.8},
            'return_on_equity': {'excellent': 30.0, 'good': 22.0, 'average': 15.0, 'poor': 8.0}
        },
        Industry.TECHNOLOGY: {
            'current_ratio': {'excellent': 3.0, 'good': 2.5, 'average': 2.0, 'poor': 1.5},
            'quick_ratio': {'excellent': 2.5, 'good': 2.0, 'average': 1.5, 'poor': 1.0},
            'net_profit_margin': {'excellent': 25.0, 'good': 18.0, 'average': 12.0, 'poor': 5.0},
            'debt_to_equity': {'excellent': 0.2, 'good': 0.5, 'average': 0.9, 'poor': 1.5},
            'asset_turnover': {'excellent': 1.8, 'good': 1.4, 'average': 1.0, 'poor': 0.6},
            'return_on_equity': {'excellent': 35.0, 'good': 25.0, 'average': 18.0, 'poor': 10.0}
        },
        Industry.AGRICULTURE: {
            'current_ratio': {'excellent': 1.8, 'good': 1.4, 'average': 1.1, 'poor': 0.8},
            'quick_ratio': {'excellent': 1.2, 'good': 0.9, 'average': 0.6, 'poor': 0.4},
            'net_profit_margin': {'excellent': 12.0, 'good': 8.0, 'average': 5.0, 'poor': 2.0},
            'debt_to_equity': {'excellent': 0.6, 'good': 1.2, 'average': 1.8, 'poor': 2.5},
            'asset_turnover': {'excellent': 1.5, 'good': 1.2, 'average': 0.9, 'poor': 0.5},
            'return_on_equity': {'excellent': 18.0, 'good': 12.0, 'average': 8.0, 'poor': 4.0}
        },
        Industry.ECOMMERCE: {
            'current_ratio': {'excellent': 2.2, 'good': 1.8, 'average': 1.4, 'poor': 1.0},
            'quick_ratio': {'excellent': 1.5, 'good': 1.2, 'average': 0.9, 'poor': 0.6},
            'net_profit_margin': {'excellent': 15.0, 'good': 10.0, 'average': 6.0, 'poor': 2.0},
            'debt_to_equity': {'excellent': 0.4, 'good': 0.9, 'average': 1.4, 'poor': 2.0},
            'asset_turnover': {'excellent': 2.8, 'good': 2.2, 'average': 1.6, 'poor': 1.0},
            'return_on_equity': {'excellent': 28.0, 'good': 20.0, 'average': 14.0, 'poor': 7.0}
        }
    }
    
    TEMPLATES = {
        'en': {
            'excellent': "Excellent - Top 20% in industry",
            'above_average': "Above Average - Top 40% in industry",
            'average': "Average - Middle 20% in industry",
            'below_average': "Below Average - Bottom 40% in industry",
            'poor': "Poor - Bottom 20% in industry"
        },
        'hi': {
            'excellent': "उत्कृष्ट - उद्योग में शीर्ष 20%",
            'above_average': "औसत से ऊपर - उद्योग में शीर्ष 40%",
            'average': "औसत - उद्योग में मध्यम 20%",
            'below_average': "औसत से कम - उद्योग में निचले 40%",
            'poor': "खराब - उद्योग में निचले 20%"
        },
        'ta': {
            'excellent': "சிறப்பானது - தொழில்துறையில் முதல் 20%",
            'above_average': "சராசரிக்கு மேல் - தொழில்துறையில் முதல் 40%",
            'average': "சராசரி - தொழில்துறையில் நடுத்தர 20%",
            'below_average': "சராசரிக்குக் கீழே - தொழில்துறையில் கீழ் 40%",
            'poor': "மோசம் - தொழில்துறையில் கீழ் 20%"
        }
    }
    
    @staticmethod
    def get_benchmark_comparison(
        metrics: Dict[str, Dict[str, float]],
        industry: str,
        language: str = 'en'
    ) -> Dict[str, Any]:
        """
        Compare business metrics against industry benchmarks
        
        Args:
            metrics: Calculated financial metrics
            industry: Business industry
            language: Translation language
            
        Returns:
            Dictionary with benchmark comparison data
        """
        # Default to services if industry not found
        industry_enum = Industry.SERVICES
        try:
            industry_enum = Industry(industry.lower())
        except ValueError:
            pass
        
        benchmarks = IndustryBenchmark.BENCHMARKS.get(
            industry_enum,
            IndustryBenchmark.BENCHMARKS[Industry.SERVICES]
        )
        
        comparison = {
            'industry': industry,
            'metrics_comparison': {},
            'overall_performance': '',
            'percentile_rank': 0
        }
        
        # Compare key metrics
        key_metrics = {
            'current_ratio': metrics['liquidity']['current_ratio'],
            'quick_ratio': metrics['liquidity']['quick_ratio'],
            'net_profit_margin': metrics['profitability']['net_profit_margin'],
            'debt_to_equity': metrics['leverage']['debt_to_equity'],
            'asset_turnover': metrics['efficiency']['asset_turnover'],
            'return_on_equity': metrics['profitability']['return_on_equity']
        }
        
        total_score = 0
        for metric_name, metric_value in key_metrics.items():
            if metric_name in benchmarks:
                benchmark = benchmarks[metric_name]
                performance = IndustryBenchmark._assess_performance(
                    metric_value,
                    benchmark,
                    metric_name
                )
                comparison['metrics_comparison'][metric_name] = {
                    'value': metric_value,
                    'industry_average': benchmark['average'],
                    'industry_excellent': benchmark['excellent'],
                    'performance': performance['level'],
                    'percentile': performance['percentile']
                }
                total_score += performance['percentile']
        
        # Calculate overall percentile
        comparison['percentile_rank'] = round(total_score / len(key_metrics))
        
        # Determine overall performance
        templates = IndustryBenchmark.TEMPLATES.get(language, IndustryBenchmark.TEMPLATES['en'])
        
        if comparison['percentile_rank'] >= 80:
            comparison['overall_performance'] = templates['excellent']
        elif comparison['percentile_rank'] >= 60:
            comparison['overall_performance'] = templates['above_average']
        elif comparison['percentile_rank'] >= 40:
            comparison['overall_performance'] = templates['average']
        elif comparison['percentile_rank'] >= 20:
            comparison['overall_performance'] = templates['below_average']
        else:
            comparison['overall_performance'] = templates['poor']
        
        return comparison
    
    @staticmethod
    def _assess_performance(
        value: float,
        benchmark: Dict[str, float],
        metric_name: str
    ) -> Dict[str, Any]:
        """Assess performance level for a metric"""
        
        # For debt_to_equity, lower is better
        if metric_name == 'debt_to_equity':
            if value <= benchmark['excellent']:
                return {'level': 'Excellent', 'percentile': 90}
            elif value <= benchmark['good']:
                return {'level': 'Good', 'percentile': 70}
            elif value <= benchmark['average']:
                return {'level': 'Average', 'percentile': 50}
            elif value <= benchmark['poor']:
                return {'level': 'Below Average', 'percentile': 30}
            else:
                return {'level': 'Poor', 'percentile': 10}
        else:
            # For other metrics, higher is better
            if value >= benchmark['excellent']:
                return {'level': 'Excellent', 'percentile': 90}
            elif value >= benchmark['good']:
                return {'level': 'Good', 'percentile': 70}
            elif value >= benchmark['average']:
                return {'level': 'Average', 'percentile': 50}
            elif value >= benchmark['poor']:
                return {'level': 'Below Average', 'percentile': 30}
            else:
                return {'level': 'Poor', 'percentile': 10}

industry_benchmark = IndustryBenchmark()
