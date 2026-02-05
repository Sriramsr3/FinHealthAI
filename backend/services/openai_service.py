from typing import Dict, Any, List, Optional
from openai import OpenAI
from config.settings import settings
import logging
import json

logger = logging.getLogger(__name__)

class OpenAIService:
    """OpenAI GPT-5.2 integration for AI-powered insights"""
    
    # Localized templates for rule-based insights
    TEMPLATES = {
        'en': {
            'liquidity_risk': "Liquidity Risk: Current ratio of {ratio:.1f} indicates potential difficulty meeting short-term obligations. Consider improving cash reserves.",
            'strong_liquidity': "Strong Liquidity: Current ratio of {ratio:.1f} shows excellent ability to cover short-term liabilities, though excess cash could be invested for growth.",
            'healthy_liquidity': "Healthy Liquidity: Current ratio of {ratio:.1f} indicates good short-term financial health with balanced working capital management.",
            'operating_loss': "Operating Loss: The business is operating at a {margin:.1f}% loss. Immediate cost restructuring and revenue optimization required.",
            'low_profitability': "Low Profitability: Net profit margin of {margin:.1f}% is below industry standards. Review pricing strategy and operational efficiency.",
            'excellent_profitability': "Excellent Profitability: Net profit margin of {margin:.1f}% demonstrates strong operational efficiency and competitive positioning.",
            'high_leverage': "High Leverage: Debt-to-equity ratio of {ratio:.1f} indicates heavy reliance on debt financing. Consider debt reduction strategies to improve financial stability.",
            'conservative_leverage': "Conservative Leverage: Low debt-to-equity ratio of {ratio:.1f} shows minimal debt burden, providing flexibility for strategic investments.",
            'cash_flow_concern': "Cash Flow Concern: Cash conversion cycle of {days:.0f} days is lengthy. Optimize inventory management and accelerate receivables collection.",
            'efficient_cash': "Efficient Cash Management: Short cash conversion cycle of {days:.0f} days indicates excellent working capital efficiency.",
            'strong_returns': "Strong Returns: Return on equity of {roe:.1f}% demonstrates excellent value creation for stakeholders.",
            'low_returns': "Low Returns: Return on equity of {roe:.1f}% suggests underutilization of capital. Explore growth opportunities or optimize asset deployment.",
            
            # Recommendations
            'rec_liquidity_1': "Improve liquidity by negotiating extended payment terms with suppliers and accelerating customer payment collection.",
            'rec_liquidity_2': "Consider a short-term working capital loan to bridge cash flow gaps.",
            'rec_profit_1': "Conduct comprehensive cost audit to identify and eliminate inefficiencies. Focus on reducing operating expenses by 10-15%.",
            'rec_profit_2': "Review pricing strategy and consider value-based pricing to improve margins.",
            'rec_debt_1': "Prioritize debt reduction through accelerated repayment or debt consolidation to improve financial stability.",
            'rec_debt_2': "Consider strategic debt financing for growth initiatives, as current leverage is conservative and provides borrowing capacity.",
            'rec_efficiency_1': "Optimize asset utilization by reviewing underperforming assets and improving operational efficiency.",
            'rec_ccc_1': "Reduce cash conversion cycle by implementing just-in-time inventory management and offering early payment discounts to customers.",
            'rec_urgent': "Urgent: Develop a 90-day cash flow improvement plan focusing on immediate cost reduction and revenue acceleration."
        },
        'hi': {
            'liquidity_risk': "तरलता जोखिम: {ratio:.1f} का वर्तमान अनुपात अल्पकालिक दायित्वों को पूरा करने में संभावित कठिनाई को दर्शाता है। नकद भंडार में सुधार पर विचार करें।",
            'strong_liquidity': "मजबूत तरलता: {ratio:.1f} का वर्तमान अनुपात अल्पकालिक देनदारियों को कवर करने की उत्कृष्ट क्षमता दर्शाता है, हालांकि अतिरिक्त नकदी को विकास के लिए निवेश किया जा सकता है।",
            'healthy_liquidity': "स्वस्थ तरलता: {ratio:.1f} का वर्तमान अनुपात संतुलित कार्यशील पूंजी प्रबंधन के साथ अच्छे अल्पकालिक वित्तीय स्वास्थ्य को इंगित करता है।",
            'operating_loss': "परिचालन हानि: व्यवसाय {margin:.1f}% की हानि पर चल रहा है। तत्काल लागत पुनर्गठन और राजस्व अनुकूलन की आवश्यकता है।",
            'low_profitability': "कम लाभप्रदता: {margin:.1f}% का शुद्ध लाभ मार्जिन उद्योग मानकों से कम है। मूल्य निर्धारण रणनीति और परिचालन दक्षता की समीक्षा करें।",
            'excellent_profitability': "उत्कृष्ट लाभप्रदता: {margin:.1f}% का शुद्ध लाभ मार्जिन मजबूत परिचालन दक्षता और प्रतिस्पर्धी स्थिति को प्रदर्शित करता है।",
            'high_leverage': "उच्च उत्तोलन: {ratio:.1f} का ऋण-से-इक्विटी अनुपात ऋण वित्तपोषण पर भारी निर्भरता को इंगित करता है। वित्तीय स्थिरता में सुधार के लिए ऋण कम करने की रणनीतियों पर विचार करें।",
            'conservative_leverage': "रूढ़िवादी उत्तोलन: {ratio:.1f} का कम ऋण-से-इक्विटी अनुपात न्यूनतम ऋण बोझ को दर्शाता है, जो रणनीतिक निवेश के लिए लचीलापन प्रदान करता है।",
            'cash_flow_concern': "नकदी प्रवाह चिंता: {days:.0f} दिनों का नकद रूपांतरण चक्र लंबा है। इन्वेंट्री प्रबंधन का अनुकूलन करें और प्राप्य संग्रह में तेजी लाएं।",
            'efficient_cash': "कुशल नकद प्रबंधन: {days:.0f} दिनों का छोटा नकद रूपांतरण चक्र उत्कृष्ट कार्यशील पूंजी दक्षता को इंगित करता है।",
            'strong_returns': "मजबूत रिटर्न: इक्विटी पर रिटर्न {roe:.1f}% हितधारकों के लिए उत्कृष्ट मूल्य निर्माण को प्रदर्शित करता है।",
            'low_returns': "कम रिटर्न: इक्विटी पर रिटर्न {roe:.1f}% पूंजी के कम उपयोग का सुझाव देता है। विकास के अवसरों का पता लगाएं या संपत्ति तैनाती का अनुकूलन करें।",

            # Recommendations
            'rec_liquidity_1': "आपूर्तिकर्ताओं के साथ विस्तारित भुगतान शर्तों पर बातचीत करके और ग्राहक भुगतान संग्रह में तेजी लाकर तरलता में सुधार करें।",
            'rec_liquidity_2': "नकदी प्रवाह के अंतराल को पाटने के लिए अल्पकालिक कार्यशील पूंजी ऋण पर विचार करें।",
            'rec_profit_1': "अक्षमताओं की पहचान करने और उन्हें खत्म करने के लिए व्यापक लागत ऑडिट करें। परिचालन व्यय को 10-15% तक कम करने पर ध्यान दें।",
            'rec_profit_2': "मूल्य निर्धारण रणनीति की समीक्षा करें और मार्जिन में सुधार के लिए मूल्य-आधारित मूल्य निर्धारण पर विचार करें।",
            'rec_debt_1': "वित्तीय स्थिरता में सुधार के लिए त्वरित पुनर्भुगतान या ऋण समेकन के माध्यम से ऋण कम करने को प्राथमिकता दें।",
            'rec_debt_2': "विकास पहलों के लिए रणनीतिक ऋण वित्तपोषण पर विचार करें, क्योंकि वर्तमान उत्तोलन रूढ़िवादी है और उधार लेने की क्षमता प्रदान करता है।",
            'rec_efficiency_1': "कम प्रदर्शन वाली संपत्तियों की समीक्षा करके और परिचालन दक्षता में सुधार करके संपत्ति के उपयोग को अनुकूलित करें।",
            'rec_ccc_1': "समय-पर-इन्वेंट्री प्रबंधन को लागू करके और ग्राहकों को शीघ्र भुगतान छूट देकर नकद रूपांतरण चक्र को कम करें।",
            'rec_urgent': "तत्काल: तत्काल लागत में कमी और राजस्व त्वरण पर ध्यान केंद्रित करते हुए 90-दिवसीय नकदी प्रवाह सुधार योजना विकसित करें।"
        },
        'ta': {
            'liquidity_risk': "பணப்புழக்க ஆபத்து: தற்போதைய விகிதம் {ratio:.1f} குறுகிய கால கடமைகளை நிறைவேற்றுவதில் சாத்தியமான சிரமத்தைக் குறிக்கிறது. பண இருப்புக்களை மேம்படுத்துவதைக் கவனியுங்கள்.",
            'strong_liquidity': "வலுவான பணப்புழக்கம்: தற்போதைய விகிதம் {ratio:.1f} குறுகிய கால பொறுப்புகளை ஈடுகட்டுவதற்கான சிறந்த திறனைக் காட்டுகிறது.",
            'healthy_liquidity': "ஆரோக்கியமான பணப்புழக்கம்: தற்போதைய விகிதம் {ratio:.1f} சீரான செயல்பாட்டு மூலதன நிர்வாகத்துடன் நல்ல குறுகிய கால நிதி ஆரோக்கியத்தைக் குறிக்கிறது.",
            'operating_loss': "செயல்பாட்டு இழப்பு: வணிகம் {margin:.1f}% இழப்பில் இயங்குகிறது. உடனடி செலவு மறுசீரமைப்பு மற்றும் வருவாய் மேம்படுத்தல் தேவை.",
            'low_profitability': "குறைந்த லாபம்: நிகர லாப வரம்பு {margin:.1f}% தொழில் தரத்தை விட குறைவாக உள்ளது. விலை நிர்ணய உத்தி மற்றும் செயல்பாட்டு செயல்திறனை மதிப்பாய்வு செய்யவும்.",
            'excellent_profitability': "சிறந்த லாபம்: நிகர லாப வரம்பு {margin:.1f}% வலுவான செயல்பாட்டு செயல்திறன் மற்றும் போட்டி நிலைப்பாட்டை நிரூபிக்கிறது.",
            'high_leverage': "அதிக நெம்புகோல்: கடன்-பங்கு விகிதம் {ratio:.1f} கடன் நிதியை பெரிதும் சார்ந்திருப்பதைக் குறிக்கிறது. நிதி நிலைத்தன்மையை மேம்படுத்த கடன் குறைப்பு உத்திகளைக் கவனியுங்கள்.",
            'conservative_leverage': "பழமைவாத நெம்புகோல்: குறைந்த கடன்-பங்கு விகிதம் {ratio:.1f} குறைந்தபட்ச கடன் சுமையைக் காட்டுகிறது, இது மூலோபாய முதலீடுகளுக்கு நெகிழ்வுத்தன்மையை வழங்குகிறது.",
            'cash_flow_concern': "பணப்புழக்க கவலை: {days:.0f} நாட்களின் பண மாற்ற சுழற்சி நீண்டது. சரக்கு நிர்வாகத்தை மேம்படுத்துங்கள் மற்றும் பெறத்தக்கவைகளை விரைவுபடுத்துங்கள்.",
            'efficient_cash': "திறமையான பண மேலாண்மை: {days:.0f} நாட்களின் குறுகிய பண மாற்ற சுழற்சி சிறந்த செயல்பாட்டு மூலதன செயல்திறனைக் குறிக்கிறது.",
            'strong_returns': "வலுவான வருமானம்: பங்குகளின் வருவாய் {roe:.1f}% பங்குதாரர்களுக்கு சிறந்த மதிப்பு உருவாக்கத்தை நிரூபிக்கிறது.",
            'low_returns': "குறைந்த வருமானம்: பங்குகளின் வருவாய் {roe:.1f}% மூலதனத்தின் பயன்பாட்டை பரிந்துரைக்கிறது. வளர்ச்சி வாய்ப்புகளை ஆராயுங்கள் அல்லது சொத்து வரிசைப்படுத்தலை மேம்படுத்தவும்.",

            # Recommendations
            'rec_liquidity_1': "சப்ளையர்களுடன் நீட்டிக்கப்பட்ட கட்டண விதிமுறைகளை பேச்சுவார்த்தை நடத்துவதன் மூலமும், வாடிக்கையாளர் கட்டண வசூலை விரைவுபடுத்துவதன் மூலமும் பணப்புழக்கத்தை மேம்படுத்தவும்.",
            'rec_liquidity_2': "பணப்புழக்க இடைவெளிகளைக் குறைக்க குறுகிய கால செயல்பாட்டு மூலதனக் கடனைக் கவனியுங்கள்.",
            'rec_profit_1': "திறமையின்மைகளை கண்டறிந்து அகற்ற விரிவான செலவு தணிக்கை நடத்தவும். செயல்பாட்டு செலவுகளை 10-15% குறைப்பதில் கவனம் செலுத்துங்கள்.",
            'rec_profit_2': "விலை நிர்ணய உத்தியை மதிப்பாய்வு செய்யவும் மற்றும் விளிம்புகளை மேம்படுத்த மதிப்பு அடிப்படையிலான விலை நிர்ணயத்தை கவனிக்கவும்.",
            'rec_debt_1': "நிதி நிலைத்தன்மையை மேம்படுத்த விரைவான திருப்பிச் செலுத்துதல் அல்லது கடன் ஒருங்கிணைப்பு மூலம் கடன் குறைப்பிற்கு முன்னுரிமை அளிக்கவும்.",
            'rec_debt_2': "வளர்ச்சி முயற்சிகளுக்கு மூலோபாய கடன் நிதியுதவியைக் கவனியுங்கள், ஏனெனில் தற்போதைய நெம்புகோல் பழமைவாதமானது மற்றும் கடன் வாங்கும் திறனை வழங்குகிறது.",
            'rec_efficiency_1': "செயல்படாத சொத்துக்களை மதிப்பாய்வு செய்து செயல்பாட்டு செயல்திறனை மேம்படுத்துவதன் மூலம் சொத்து பயன்பாட்டை மேம்படுத்தவும்.",
            'rec_ccc_1': "சரியான நேர சரக்கு நிர்வாகத்தை செயல்படுத்துவதன் மூலமும் வாடிக்கையாளர்களுக்கு முன்கூட்டியே கட்டண தள்ளுபடியை வழங்குவதன் மூலமும் பண மாற்ற சுழற்சியைக் குறைக்கவும்.",
            'rec_urgent': "அவசரம்: உடனடி செலவு குறைப்பு மற்றும் வருவாய் முடுக்கம் ஆகியவற்றில் கவனம் செலுத்தும் 90 நாள் பணப்புழக்க மேம்பாட்டுத் திட்டத்தை உருவாக்குங்கள்."
        }
    }
    
    def __init__(self):
        self.client = None
        self.enabled = settings.OPENAI_ENABLED
        
        if self.enabled:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI service initialized successfully")
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}. Falling back to rule-based insights.")
                self.enabled = False
    
    def generate_insights(
        self,
        financial_data: Dict[str, float],
        metrics: Dict[str, Dict[str, float]],
        industry: str,
        business_type: str,
        language: str = 'en'
    ) -> List[str]:
        """Generate AI-powered financial insights"""
        if self.enabled and self.client:
            try:
                return self._generate_ai_insights(financial_data, metrics, industry, business_type)
            except Exception as e:
                logger.error(f"OpenAI API error: {e}. Falling back to rule-based insights.")
                return self._generate_rule_based_insights(financial_data, metrics, industry, language)
        else:
            return self._generate_rule_based_insights(financial_data, metrics, industry, language)
    
    def _generate_ai_insights(
        self,
        financial_data: Dict[str, float],
        metrics: Dict[str, Dict[str, float]],
        industry: str,
        business_type: str
    ) -> List[str]:
        """Generate insights using OpenAI GPT-5.2"""
        # Note: True multilingual support here would require passing language to the prompt
        
        prompt = f"""You are a financial analyst specializing in SME financial health assessment.

Business Profile:
- Industry: {industry}
- Business Type: {business_type}

Financial Data:
{json.dumps(financial_data, indent=2)}

Calculated Metrics:
{json.dumps(metrics, indent=2)}

Task: Provide 4-6 concise, actionable insights about this business's financial health. Focus on:
1. Key strengths and weaknesses
2. Industry-specific observations
3. Cash flow and liquidity concerns
4. Profitability trends
5. Risk factors

Format: Return ONLY a JSON array of strings, each insight being one sentence. Example:
["Insight 1 here", "Insight 2 here", "Insight 3 here"]
"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing insights for SME businesses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Parse JSON response
            insights = json.loads(content)
            return insights if isinstance(insights, list) else [content]
            
        except json.JSONDecodeError:
            # If response isn't valid JSON, return as single insight
            return [response.choices[0].message.content.strip()]
        except Exception as e:
            logger.error(f"Error generating AI insights: {e}")
            raise
    
    def _generate_rule_based_insights(
        self,
        financial_data: Dict[str, float],
        metrics: Dict[str, Dict[str, float]],
        industry: str,
        language: str = 'en'
    ) -> List[str]:
        """Generate insights using rule-based logic (fallback)"""
        insights = []
        
        # Select defaults if language not supported
        templates = self.TEMPLATES.get(language, self.TEMPLATES['en'])
        
        # Liquidity insights
        current_ratio = metrics['liquidity']['current_ratio']
        if current_ratio < 1.0:
            insights.append(templates['liquidity_risk'].format(ratio=current_ratio))
        elif current_ratio > 2.5:
            insights.append(templates['strong_liquidity'].format(ratio=current_ratio))
        else:
            insights.append(templates['healthy_liquidity'].format(ratio=current_ratio))
        
        # Profitability insights
        npm = metrics['profitability']['net_profit_margin']
        if npm < 0:
            insights.append(templates['operating_loss'].format(margin=abs(npm)))
        elif npm < 5:
            insights.append(templates['low_profitability'].format(margin=npm))
        elif npm > 15:
            insights.append(templates['excellent_profitability'].format(margin=npm))
        
        # Leverage insights
        debt_to_equity = metrics['leverage']['debt_to_equity']
        if debt_to_equity > 2.0:
            insights.append(templates['high_leverage'].format(ratio=debt_to_equity))
        elif debt_to_equity < 0.5:
            insights.append(templates['conservative_leverage'].format(ratio=debt_to_equity))
        
        # Working capital insights
        ccc = metrics['working_capital']['cash_conversion_cycle']
        if ccc > 90:
            insights.append(templates['cash_flow_concern'].format(days=ccc))
        elif ccc < 30:
            insights.append(templates['efficient_cash'].format(days=ccc))
        
        # ROE insight
        roe = metrics['profitability']['return_on_equity']
        if roe > 20:
            insights.append(templates['strong_returns'].format(roe=roe))
        elif roe < 5 and roe > 0:
            insights.append(templates['low_returns'].format(roe=roe))
        
        return insights[:6]  # Return max 6 insights
    
    def generate_recommendations(
        self,
        insights: List[str],
        metrics: Dict[str, Dict[str, float]],
        risk_level: str,
        industry: str,
        language: str = 'en'
    ) -> List[str]:
        """Generate actionable recommendations"""
        if self.enabled and self.client:
            try:
                return self._generate_ai_recommendations(insights, metrics, risk_level, industry)
            except Exception as e:
                logger.error(f"OpenAI API error: {e}. Falling back to rule-based recommendations.")
                return self._generate_rule_based_recommendations(metrics, risk_level, language)
        else:
            return self._generate_rule_based_recommendations(metrics, risk_level, language)
    
    def _generate_ai_recommendations(
        self,
        insights: List[str],
        metrics: Dict[str, Dict[str, float]],
        risk_level: str,
        industry: str
    ) -> List[str]:
        """Generate recommendations using OpenAI GPT-5.2"""
        
        prompt = f"""Based on the following financial insights for a {industry} business with {risk_level} risk level:

Insights:
{json.dumps(insights, indent=2)}

Key Metrics:
{json.dumps(metrics, indent=2)}

Task: Provide 4-6 specific, actionable recommendations to improve financial health. Focus on:
1. Immediate actions for critical issues
2. Medium-term strategic improvements
3. Growth opportunities
4. Risk mitigation strategies

Format: Return ONLY a JSON array of strings. Example:
["Recommendation 1", "Recommendation 2", "Recommendation 3"]
"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a financial advisor providing actionable recommendations for businesses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            recommendations = json.loads(content)
            return recommendations if isinstance(recommendations, list) else [content]
            
        except json.JSONDecodeError:
            return [response.choices[0].message.content.strip()]
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
            raise
    
    def _generate_rule_based_recommendations(
        self,
        metrics: Dict[str, Dict[str, float]],
        risk_level: str,
        language: str = 'en'
    ) -> List[str]:
        """Generate recommendations using rule-based logic"""
        recommendations = []
        
        # Select defaults if language not supported
        templates = self.TEMPLATES.get(language, self.TEMPLATES['en'])
        
        # Liquidity recommendations
        current_ratio = metrics['liquidity']['current_ratio']
        if current_ratio < 1.0:
            recommendations.append(templates['rec_liquidity_1'])
            recommendations.append(templates['rec_liquidity_2'])
        
        # Profitability recommendations
        npm = metrics['profitability']['net_profit_margin']
        if npm < 5:
            recommendations.append(templates['rec_profit_1'])
            recommendations.append(templates['rec_profit_2'])
        
        # Leverage recommendations
        debt_to_equity = metrics['leverage']['debt_to_equity']
        if debt_to_equity > 2.0:
            recommendations.append(templates['rec_debt_1'])
        elif debt_to_equity < 0.3:
            recommendations.append(templates['rec_debt_2'])
        
        # Efficiency recommendations
        asset_turnover = metrics['efficiency']['asset_turnover']
        if asset_turnover < 1.0:
            recommendations.append(templates['rec_efficiency_1'])
        
        # Working capital recommendations
        ccc = metrics['working_capital']['cash_conversion_cycle']
        if ccc > 60:
            recommendations.append(templates['rec_ccc_1'])
        
        # Risk-specific recommendations
        if risk_level in ["High", "Critical"]:
            recommendations.append(templates['rec_urgent'])
        
        return recommendations[:6]

openai_service = OpenAIService()
