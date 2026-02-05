from typing import Dict, Any, List
from datetime import datetime, timedelta
import calendar

class TaxCompliance:
    """Tax compliance checking and GST integration service"""
    
    # GST tax slabs
    GST_SLABS = {
        'exempt': 0,
        'low': 5,
        'standard': 12,
        'high': 18,
        'luxury': 28
    }

    # Localized templates
    TEMPLATES = {
        'en': {
            'tip_docs': "Maintain proper documentation of all business expenses to maximize deductions",
            'tip_investment': "Consider investing in tax-saving instruments like PPF, ELSS, or NPS for additional deductions",
            'tip_composition': "Consider opting for composition scheme under GST if eligible to reduce compliance burden",
            'tip_80jjaa': "Explore Section 80JJAA deductions for new employee hiring (30% of additional wages)",
            'tip_capex': "Consider capital expenditure before year-end for depreciation benefits",
            'tip_32ad': "Claim deduction under Section 32AD for investment in new plant and machinery",
            'tip_rd': "Utilize Section 35(2AB) for R&D expenditure deductions (150% weighted deduction)",
            'tip_lower_rate': "Companies with turnover < ₹400 crore can opt for 22% tax rate (without exemptions)"
        },
        'hi': {
            'tip_docs': "कटौती को अधिकतम करने के लिए सभी व्यावसायिक खर्चों का उचित दस्तावेज़ीकरण बनाए रखें",
            'tip_investment': "अतिरिक्त कटौती के लिए पीपीएफ, ईएलएसएस या एनपीएस जैसे कर-बचत साधनों में निवेश करने पर विचार करें",
            'tip_composition': "यदि अनुपालन बोझ को कम करने के लिए पात्र हैं, तो जीएसटी के तहत संरचना योजना चुनने पर विचार करें",
            'tip_80jjaa': "नए कर्मचारी को काम पर रखने के लिए धारा 80JJAA कटौती का पता लगाएं (अतिरिक्त मजदूरी का 30%)",
            'tip_capex': "मूल्यह्रास लाभ के लिए साल के अंत से पहले पूंजीगत व्यय पर विचार करें",
            'tip_32ad': "नए संयंत्र और मशीनरी में निवेश के लिए धारा 32AD के तहत कटौती का दावा करें",
            'tip_rd': "आर एंड डी व्यय कटौती (150% भारित कटौती) के लिए धारा 35(2AB) का उपयोग करें",
            'tip_lower_rate': "< ₹400 करोड़ के कारोबार वाली कंपनियां 22% कर दर (छूट के बिना) का विकल्प चुन सकती हैं"
        },
        'ta': {
            'tip_docs': "விலக்குகளை அதிகரிக்க அனைத்து வணிக செலவுகளின் முறையான ஆவணங்களை பராமரிக்கவும்",
            'tip_investment': "கூடுதல் விலக்குகளுக்கு பிபிஎஃப், ஈஎல்எஸ்எஸ் அல்லது என்பிஎஸ் போன்ற வரி சேமிப்பு கருவிகளில் முதலீடு செய்வதைக் கவனியுங்கள்",
            'tip_composition': "இணக்க சுமையை குறைக்க தகுதியுடையவராக இருந்தால் ஜிஎஸ்டியின் கீழ் கலவை திட்டத்தைத் தேர்ந்தெடுப்பதைக் கவனியுங்கள்",
            'tip_80jjaa': "புதிய பணியாளர் நியமனத்திற்கு பிரிவு 80JJAA விலக்குகளை ஆராயுங்கள் (கூடுதல் ஊதியத்தில் 30%)",
            'tip_capex': "தேய்மான நன்மைகளுக்கு ஆண்டு இறுதிக்குள் மூலதன செலவினங்களைக் கவனியுங்கள்",
            'tip_32ad': "புதிய ஆலை மற்றும் இயந்திரங்களில் முதலீடு செய்வதற்கு பிரிவு 32AD இன் கீழ் விலக்கு கோருங்கள்",
            'tip_rd': "ஆர் & டி செலவின விலக்குகளுக்கு பிரிவு 35(2AB) ஐப் பயன்படுத்தவும் (150% எடையுள்ள விலக்கு)",
            'tip_lower_rate': "< ₹400 கோடி வருவாய் உள்ள நிறுவனங்கள் 22% வரி விகிதத்தைத் (விலக்குகள் இல்லாமல்) தேர்வு செய்யலாம்"
        }
    }
    
    @staticmethod
    def check_compliance(
        financial_data: Dict[str, float],
        industry: str,
        business_type: str,
        language: str = 'en'
    ) -> Dict[str, Any]:
        """
        Check tax compliance status
        """
        revenue = financial_data.get('revenue', 0)
        net_income = financial_data.get('net_income', 0)
        
        compliance_report = {
            'gst_status': TaxCompliance._check_gst_compliance(revenue, industry),
            'income_tax_estimate': TaxCompliance._estimate_income_tax(net_income, business_type),
            'filing_deadlines': TaxCompliance._get_filing_deadlines(),
            'tax_optimization_tips': TaxCompliance._get_tax_optimization_tips(
                financial_data,
                industry,
                business_type,
                language
            ),
            'compliance_score': 0
        }
        
        # Calculate compliance score
        compliance_score = 100
        if revenue > 2000000 and not compliance_report['gst_status']['registered']:
            compliance_score -= 30
        
        compliance_report['compliance_score'] = compliance_score
        
        return compliance_report
    
    @staticmethod
    def _check_gst_compliance(revenue: float, industry: str) -> Dict[str, Any]:
        """Check GST registration and compliance status"""
        
        # GST registration threshold (₹20 lakhs for most states, ₹10 lakhs for special category states)
        gst_threshold = 2000000  # ₹20 lakhs
        
        status = {
            'registered': revenue > gst_threshold,
            'threshold': gst_threshold,
            'annual_revenue': revenue,
            'registration_required': revenue > gst_threshold,
            'applicable_rate': TaxCompliance._get_gst_rate(industry),
            'estimated_gst_liability': 0,
            'filing_frequency': 'Monthly' if revenue > 5000000 else 'Quarterly',
            'compliance_status': 'Compliant'
        }
        
        if status['registered']:
            # Estimate GST liability (simplified)
            gst_rate = status['applicable_rate'] / 100
            status['estimated_gst_liability'] = round(revenue * gst_rate * 0.15, 2)  # Approximate
        
        if revenue > gst_threshold and not status['registered']:
            status['compliance_status'] = 'Non-Compliant - Registration Required'
        
        return status
    
    @staticmethod
    def _get_gst_rate(industry: str) -> float:
        """Get applicable GST rate for industry"""
        industry_rates = {
            'manufacturing': 18,
            'retail': 12,
            'services': 18,
            'technology': 18,
            'agriculture': 5,
            'ecommerce': 18,
            'logistics': 18,
            'healthcare': 12,
            'hospitality': 18,
            'construction': 18
        }
        return industry_rates.get(industry.lower(), 18)
    
    @staticmethod
    def _estimate_income_tax(net_income: float, business_type: str) -> Dict[str, Any]:
        """Estimate income tax liability"""
        
        # Corporate tax rates (simplified)
        tax_rates = {
            'private_limited': 0.25,  # 25% for companies
            'public_limited': 0.25,
            'llp': 0.30,  # 30% for LLP
            'partnership': 0.30,
            'sole_proprietorship': 0.30  # Individual tax slab (simplified)
        }
        
        tax_rate = tax_rates.get(business_type.lower(), 0.30)
        
        # Calculate tax (simplified - doesn't account for deductions)
        taxable_income = max(0, net_income)
        estimated_tax = taxable_income * tax_rate
        
        return {
            'taxable_income': round(taxable_income, 2),
            'applicable_rate': f"{tax_rate * 100}%",
            'estimated_tax_liability': round(estimated_tax, 2),
            'effective_tax_rate': round((estimated_tax / net_income * 100) if net_income > 0 else 0, 2)
        }
    
    @staticmethod
    def _get_filing_deadlines() -> List[Dict[str, str]]:
        """Get upcoming tax filing deadlines"""
        today = datetime.now()
        
        # Helper to safely get the last day of the current month
        last_day = calendar.monthrange(today.year, today.month)[1]
        
        deadlines = [
            {
                'type': 'GST Return (GSTR-3B)',
                # 20th of the month logic. Safe to use min(20, last_day) just in case, though 20 is safe for all months.
                'deadline': (today.replace(day=min(20, last_day)) + timedelta(days=30)).strftime('%Y-%m-%d'),
                'frequency': 'Monthly',
                'penalty_for_delay': '₹50/day (max ₹5,000)'
            },
            {
                'type': 'Income Tax Return',
                'deadline': f"{today.year}-07-31",
                'frequency': 'Annual',
                'penalty_for_delay': '₹5,000 (if filed before Dec 31), ₹10,000 (after)'
            },
            {
                'type': 'TDS Return',
                # Was: today.replace(day=31) which caused error in Feb
                # Fixed: Use actual last day of month
                'deadline': (today.replace(day=last_day) + timedelta(days=30)).strftime('%Y-%m-%d'),
                'frequency': 'Quarterly',
                'penalty_for_delay': '₹200/day'
            },
            {
                'type': 'Annual GST Return (GSTR-9)',
                'deadline': f"{today.year}-12-31",
                'frequency': 'Annual',
                'penalty_for_delay': '₹100/day (max ₹0.25% of turnover)'
            }
        ]
        
        return deadlines
    
    @staticmethod
    def _get_tax_optimization_tips(
        financial_data: Dict[str, float],
        industry: str,
        business_type: str,
        language: str = 'en'
    ) -> List[str]:
        """Generate tax optimization suggestions"""
        tips = []
        
        revenue = financial_data.get('revenue', 0)
        net_income = financial_data.get('net_income', 0)
        
        # Select defaults if language not supported
        templates = TaxCompliance.TEMPLATES.get(language, TaxCompliance.TEMPLATES['en'])
        
        # General tips
        tips.append(templates['tip_docs'])
        tips.append(templates['tip_investment'])
        
        # Revenue-based tips
        if revenue > 5000000:
            tips.append(templates['tip_composition'])
        
        # Profitability-based tips
        if net_income > 1000000:
            tips.append(templates['tip_80jjaa'])
            tips.append(templates['tip_capex'])
        
        # Industry-specific tips
        if industry.lower() == 'manufacturing':
            tips.append(templates['tip_32ad'])
        elif industry.lower() == 'technology':
            tips.append(templates['tip_rd'])
        
        # Business type tips
        if business_type.lower() in ['private_limited', 'public_limited']:
            tips.append(templates['tip_lower_rate'])
        
        return tips

tax_compliance = TaxCompliance()
