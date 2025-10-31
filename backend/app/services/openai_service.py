from openai import AsyncOpenAI
from typing import Dict, List
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """OpenAI service for email analysis and classification"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def analyze_email(self, email_data: Dict) -> Dict:
        """
        Analyze email using GPT-4 to extract:
        - Priority level (High/Medium/Low)
        - Category (Action Required/Info/Meeting/Spam)
        - Tasks and deadlines
        - Sentiment
        - Key entities (people, companies, dates)
        """
        
        prompt = f"""Analyze this email and provide structured information:

Subject: {email_data.get('subject', '')}
From: {email_data.get('from', '')}
Body: {email_data.get('body', '')[:2000]}

Provide analysis in JSON format:
{{
    "priority": "High/Medium/Low",
    "category": "Action Required/Info/Meeting/Spam/Newsletter",
    "sentiment": "Positive/Neutral/Negative",
    "requires_response": true/false,
    "tasks": ["list of action items"],
    "deadlines": ["list of deadlines with dates"],
    "key_people": ["names mentioned"],
    "key_companies": ["companies mentioned"],
    "meeting_info": {{
        "is_meeting": true/false,
        "date": "extracted date",
        "time": "extracted time",
        "location": "location or meeting link"
    }},
    "summary": "one-line summary",
    "suggested_reply": "brief suggested response if action required"
}}"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert email analyst. Provide accurate, structured analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            logger.info(f"Email analyzed: {email_data.get('subject', 'No subject')}")
            return analysis
            
        except Exception as error:
            logger.error(f"OpenAI analysis error: {error}")
            return self._default_analysis()
    
    async def batch_analyze_emails(self, emails: List[Dict]) -> List[Dict]:
        """Analyze multiple emails in batch"""
        results = []
        for email in emails:
            analysis = await self.analyze_email(email)
            results.append({
                **email,
                'analysis': analysis
            })
        return results
    
    async def generate_daily_summary(self, analyzed_emails: List[Dict]) -> str:
        """Generate daily intelligence report summary"""
        
        prompt = f"""Create a concise daily email intelligence report based on these analyzed emails:

Total Emails: {len(analyzed_emails)}
High Priority: {sum(1 for e in analyzed_emails if e.get('analysis', {}).get('priority') == 'High')}
Action Required: {sum(1 for e in analyzed_emails if e.get('analysis', {}).get('requires_response'))}
Meetings: {sum(1 for e in analyzed_emails if e.get('analysis', {}).get('meeting_info', {}).get('is_meeting'))}

Provide a professional summary with:
1. Executive Summary
2. Top Priority Actions
3. Upcoming Meetings
4. Key Insights
5. Time Saved Estimate

Format in markdown."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an executive assistant creating daily briefings."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as error:
            logger.error(f"Summary generation error: {error}")
            return "Error generating summary"
    
    async def detect_phishing(self, email_data: Dict) -> Dict:
        """Detect potential phishing or security threats"""
        
        prompt = f"""Analyze this email for security threats:

From: {email_data.get('from', '')}
Subject: {email_data.get('subject', '')}
Body: {email_data.get('body', '')[:1000]}

Check for:
- Suspicious sender
- Phishing indicators
- Malicious links
- Urgency tactics
- Impersonation

Respond in JSON:
{{
    "is_suspicious": true/false,
    "threat_level": "High/Medium/Low/None",
    "indicators": ["list of red flags"],
    "recommendation": "action to take"
}}"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing emails for threats."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as error:
            logger.error(f"Phishing detection error: {error}")
            return {"is_suspicious": False, "threat_level": "None"}
    
    def _default_analysis(self) -> Dict:
        """Return default analysis structure on error"""
        return {
            "priority": "Medium",
            "category": "Info",
            "sentiment": "Neutral",
            "requires_response": False,
            "tasks": [],
            "deadlines": [],
            "key_people": [],
            "key_companies": [],
            "meeting_info": {"is_meeting": False},
            "summary": "Analysis unavailable",
            "suggested_reply": ""
        }
