import openai
from typing import List, Dict, Any, Optional
from app.config import settings
from app.schemas.chat import SymptomAnalysisResponse, Condition, TriageAdvice
import json
import logging

logger = logging.getLogger(__name__)

# Initialize OpenAI client
if settings.openai_api_key:
    openai.api_key = settings.openai_api_key


class AIService:
    def __init__(self):
        self.model = settings.openai_model
        self.client = openai.OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    async def analyze_symptoms(self, request_data: dict) -> SymptomAnalysisResponse:
        """Analyze symptoms and provide medical insights."""
        if not self.client:
            raise Exception("OpenAI API key not configured")
        
        try:
            # Prepare the prompt for symptom analysis
            prompt = self._create_symptom_analysis_prompt(request_data)
            
            # Call OpenAI API
            response = await self._call_openai_api(prompt)
            
            # Parse and structure the response
            return self._parse_symptom_response(response, request_data)
            
        except Exception as e:
            logger.error(f"Error in symptom analysis: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")
    
    def _create_symptom_analysis_prompt(self, request_data: dict) -> str:
        """Create a structured prompt for symptom analysis."""
        symptoms = request_data.get("symptoms", [])
        age = request_data.get("age")
        gender = request_data.get("gender")
        medical_history = request_data.get("medical_history", [])
        medications = request_data.get("current_medications", [])
        additional_info = request_data.get("additional_info", "")
        
        prompt = f"""
You are a medical AI assistant. Analyze the following symptoms and provide a structured response.

PATIENT INFORMATION:
- Age: {age if age else 'Not specified'}
- Gender: {gender if gender else 'Not specified'}
- Symptoms: {', '.join(symptoms)}
- Medical History: {', '.join(medical_history) if medical_history else 'None provided'}
- Current Medications: {', '.join(medications) if medications else 'None'}
- Additional Information: {additional_info if additional_info else 'None'}

Please provide a JSON response with the following structure:
{{
    "conditions": [
        {{
            "name": "Condition Name",
            "probability": 0.85,
            "description": "Brief description of the condition",
            "severity": "mild|moderate|severe"
        }}
    ],
    "triage_advice": {{
        "urgency": "low|medium|high|emergency",
        "recommendation": "Specific recommendation for care",
        "timeframe": "When to seek care (e.g., 'within 24 hours')"
    }},
    "disclaimer": "This is not a substitute for professional medical advice. Always consult a healthcare provider.",
    "confidence_score": 0.75,
    "follow_up_recommendations": [
        "Specific follow-up action 1",
        "Specific follow-up action 2"
    ]
}}

IMPORTANT GUIDELINES:
1. Be conservative in your assessments
2. Always recommend consulting a healthcare provider for serious symptoms
3. If symptoms suggest emergency conditions, mark urgency as "emergency"
4. Provide probabilities as decimal numbers (0.0 to 1.0)
5. Include appropriate disclaimers
6. Focus on the most likely 3-5 conditions
7. Be specific about timeframes for seeking care
"""
        return prompt
    
    async def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API with the prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical AI assistant. Provide accurate, helpful, and responsible medical information. Always recommend consulting healthcare professionals for serious concerns."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to get AI response: {str(e)}")
    
    def _parse_symptom_response(self, response: str, request_data: dict) -> SymptomAnalysisResponse:
        """Parse OpenAI response into structured format."""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            data = json.loads(json_str)
            
            # Parse conditions
            conditions = [
                Condition(
                    name=cond["name"],
                    probability=cond["probability"],
                    description=cond["description"],
                    severity=cond["severity"]
                )
                for cond in data.get("conditions", [])
            ]
            
            # Parse triage advice
            triage_data = data.get("triage_advice", {})
            triage_advice = TriageAdvice(
                urgency=triage_data.get("urgency", "medium"),
                recommendation=triage_data.get("recommendation", "Consult a healthcare provider"),
                timeframe=triage_data.get("timeframe", "As soon as possible")
            )
            
            return SymptomAnalysisResponse(
                conditions=conditions,
                triage_advice=triage_advice,
                disclaimer=data.get("disclaimer", "This is not a substitute for professional medical advice."),
                confidence_score=data.get("confidence_score", 0.5),
                follow_up_recommendations=data.get("follow_up_recommendations", [])
            )
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            # Return a safe default response
            return SymptomAnalysisResponse(
                conditions=[
                    Condition(
                        name="Unable to analyze",
                        probability=0.0,
                        description="Unable to process symptoms at this time",
                        severity="unknown"
                    )
                ],
                triage_advice=TriageAdvice(
                    urgency="medium",
                    recommendation="Please consult a healthcare provider",
                    timeframe="As soon as possible"
                ),
                disclaimer="This is not a substitute for professional medical advice. Please consult a healthcare provider.",
                confidence_score=0.0,
                follow_up_recommendations=["Consult a healthcare provider for proper diagnosis"]
            )
    
    async def generate_chat_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Generate a conversational response for the chatbot."""
        if not self.client:
            return "I'm sorry, I'm not available right now. Please try again later."
        
        try:
            system_prompt = """You are a helpful medical assistant chatbot. Provide general health information and guidance, but always recommend consulting healthcare professionals for medical concerns. Be empathetic, clear, and helpful."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if context:
                messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
            
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return "I'm sorry, I'm having trouble processing your request. Please try again later."


# Global AI service instance
ai_service = AIService()
