import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.config import settings
from app.schemas.chat import SymptomAnalysisResponse, Condition, TriageAdvice
import json
import logging

logger = logging.getLogger(__name__)

# Initialize Gemini client
genai.configure(api_key=settings.gemini_api_key)


class GeminiAIService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.gemini_model)
        self._init_safety_settings()

    def _init_safety_settings(self):
        """Initialize safety settings for the Gemini model."""
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    
    async def analyze_symptoms(self, request_data: dict) -> SymptomAnalysisResponse:
        """Analyze symptoms and provide medical insights using Gemini."""
        try:
            # Prepare the prompt for symptom analysis
            prompt = self._create_symptom_analysis_prompt(request_data)
            
            # Generate response from Gemini
            response = await self._generate_response(prompt)
            
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

Patient Information:
- Age: {age}
- Gender: {gender}
- Symptoms: {', '.join(symptoms)}
- Medical History: {', '.join(medical_history)}
- Current Medications: {', '.join(medications)}
- Additional Information: {additional_info}

Please provide a detailed analysis in the following JSON structure:
{{
    "possible_conditions": [
        {{
            "name": "condition name",
            "confidence": "probability percentage",
            "description": "brief description",
            "common_symptoms": ["symptom1", "symptom2"]
        }}
    ],
    "triage_level": "EMERGENCY|URGENT|NON_URGENT",
    "triage_advice": {{
        "recommendation": "what the patient should do",
        "timeframe": "when they should seek care",
        "care_level": "what type of care they need"
    }},
    "lifestyle_recommendations": ["recommendation1", "recommendation2"],
    "warning_signs": ["sign1", "sign2"]
}}
"""
        return prompt

    async def _generate_response(self, prompt: str) -> str:
        """Generate response from Gemini model."""
        try:
            response = await self.model.generate_content_async(
                prompt,
                safety_settings=self.safety_settings,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise

    def _parse_symptom_response(self, response: str, request_data: dict) -> SymptomAnalysisResponse:
        """Parse and structure the Gemini response."""
        try:
            response_data = json.loads(response)
            
            conditions = [
                Condition(
                    name=cond["name"],
                    confidence=cond["confidence"],
                    description=cond["description"],
                    common_symptoms=cond["common_symptoms"]
                )
                for cond in response_data["possible_conditions"]
            ]
            
            triage_advice = TriageAdvice(
                recommendation=response_data["triage_advice"]["recommendation"],
                timeframe=response_data["triage_advice"]["timeframe"],
                care_level=response_data["triage_advice"]["care_level"]
            )
            
            return SymptomAnalysisResponse(
                possible_conditions=conditions,
                triage_level=response_data["triage_level"],
                triage_advice=triage_advice,
                lifestyle_recommendations=response_data["lifestyle_recommendations"],
                warning_signs=response_data["warning_signs"]
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            raise Exception("Invalid response format from AI service")
        except KeyError as e:
            logger.error(f"Missing key in response: {str(e)}")
            raise Exception("Incomplete response from AI service")