from typing import Dict, Any

class TranslationService:
    """Multilingual support service for English and Hindi"""
    
    TRANSLATIONS = {
        'en': {
            # UI Labels
            'financial_health_score': 'Financial Health Score',
            'risk_level': 'Risk Level',
            'insights': 'AI Insights',
            'recommendations': 'Strategic Recommendations',
            'metrics': 'Key Metrics',
            'current_ratio': 'Current Ratio',
            'quick_ratio': 'Quick Ratio',
            'net_profit_margin': 'Net Profit Margin',
            'debt_to_equity': 'Debt to Equity',
            'return_on_equity': 'Return on Equity',
            'asset_turnover': 'Asset Turnover',
            'cash_conversion_cycle': 'Cash Conversion Cycle',
            'working_capital': 'Working Capital',
            
            # Risk Levels
            'Low': 'Low',
            'Moderate': 'Moderate',
            'High': 'High',
            'Critical': 'Critical',
            
            # Business Types
            'manufacturing': 'Manufacturing',
            'retail': 'Retail',
            'services': 'Services',
            'technology': 'Technology',
            'agriculture': 'Agriculture',
            'ecommerce': 'E-commerce',
            
            # Common Phrases
            'upload_document': 'Upload Financial Document',
            'analyze': 'Analyze',
            'export_report': 'Export Report',
            'cash_flow_forecast': 'Cash Flow Forecast',
            'industry_benchmark': 'Industry Benchmark',
            'tax_compliance': 'Tax Compliance',
            'product_recommendations': 'Financial Product Recommendations'
        },
        'hi': {
            # UI Labels
            'financial_health_score': 'वित्तीय स्वास्थ्य स्कोर',
            'risk_level': 'जोखिम स्तर',
            'insights': 'एआई अंतर्दृष्टि',
            'recommendations': 'रणनीतिक सिफारिशें',
            'metrics': 'मुख्य मेट्रिक्स',
            'current_ratio': 'वर्तमान अनुपात',
            'quick_ratio': 'त्वरित अनुपात',
            'net_profit_margin': 'शुद्ध लाभ मार्जिन',
            'debt_to_equity': 'ऋण से इक्विटी',
            'return_on_equity': 'इक्विटी पर रिटर्न',
            'asset_turnover': 'संपत्ति टर्नओवर',
            'cash_conversion_cycle': 'नकद रूपांतरण चक्र',
            'working_capital': 'कार्यशील पूंजी',
            
            # Risk Levels
            'Low': 'कम',
            'Moderate': 'मध्यम',
            'High': 'उच्च',
            'Critical': 'गंभीर',
            
            # Business Types
            'manufacturing': 'विनिर्माण',
            'retail': 'खुदरा',
            'services': 'सेवाएं',
            'technology': 'प्रौद्योगिकी',
            'agriculture': 'कृषि',
            'ecommerce': 'ई-कॉमर्स',
            
            # Common Phrases
            'upload_document': 'वित्तीय दस्तावेज़ अपलोड करें',
            'analyze': 'विश्लेषण करें',
            'export_report': 'रिपोर्ट निर्यात करें',
            'cash_flow_forecast': 'नकदी प्रवाह पूर्वानुमान',
            'industry_benchmark': 'उद्योग बेंचमार्क',
            'tax_compliance': 'कर अनुपालन',
            'product_recommendations': 'वित्तीय उत्पाद सिफारिशें'
        },
        'ta': {
            # Tamil translations (basic set)
            'financial_health_score': 'நிதி சுகாதார மதிப்பெண்',
            'risk_level': 'இடர் நிலை',
            'insights': 'AI நுண்ணறிவுகள்',
            'recommendations': 'பரிந்துரைகள்',
            'metrics': 'முக்கிய அளவீடுகள்',
            'Low': 'குறைவு',
            'Moderate': 'மிதமான',
            'High': 'உயர்',
            'Critical': 'முக்கியமான',
            'analyze': 'பகுப்பாய்வு செய்',
            'export_report': 'அறிக்கையை ஏற்றுமதி செய்'
        },
        'te': {
            # Telugu translations (basic set)
            'financial_health_score': 'ఆర్థిక ఆరోగ్య స్కోర్',
            'risk_level': 'రిస్క్ స్థాయి',
            'insights': 'AI అంతర్దృష్టులు',
            'recommendations': 'సిఫార్సులు',
            'metrics': 'కీలక మెట్రిక్స్',
            'Low': 'తక్కువ',
            'Moderate': 'మితమైన',
            'High': 'అధిక',
            'Critical': 'క్లిష్టమైన',
            'analyze': 'విశ్లేషించండి',
            'export_report': 'నివేదికను ఎగుమతి చేయండి'
        }
    }
    
    @staticmethod
    def translate(key: str, language: str = 'en') -> str:
        """
        Translate a key to the specified language
        
        Args:
            key: Translation key
            language: Target language code (en, hi, ta, te)
            
        Returns:
            Translated string
        """
        lang_dict = TranslationService.TRANSLATIONS.get(language, TranslationService.TRANSLATIONS['en'])
        return lang_dict.get(key, key)
    
    @staticmethod
    def get_all_translations(language: str = 'en') -> Dict[str, str]:
        """Get all translations for a language"""
        return TranslationService.TRANSLATIONS.get(language, TranslationService.TRANSLATIONS['en'])
    
    @staticmethod
    def translate_dict(data: Dict[str, Any], language: str = 'en') -> Dict[str, Any]:
        """
        Translate dictionary keys
        
        Args:
            data: Dictionary to translate
            language: Target language
            
        Returns:
            Dictionary with translated keys
        """
        if language == 'en':
            return data
        
        translated = {}
        for key, value in data.items():
            translated_key = TranslationService.translate(key, language)
            if isinstance(value, dict):
                translated[translated_key] = TranslationService.translate_dict(value, language)
            elif isinstance(value, list):
                translated[translated_key] = value
            else:
                # Try to translate value if it's a known term
                if isinstance(value, str):
                    translated[translated_key] = TranslationService.translate(value, language)
                else:
                    translated[translated_key] = value
        
        return translated

translation_service = TranslationService()
