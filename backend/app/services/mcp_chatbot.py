import sys
print(sys.path)
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.config import settings
from app.database import get_async_mongo_collection
from app.schemas.chat import ChatMessage, ChatResponse, SymptomAnalysisResponse, Condition, TriageAdvice
import google.generativeai as genai
import anthropic
import openai

logger = logging.getLogger(__name__)


class MCPChatbotService:
    """MCP-powered medical chatbot for symptom detection and medical assistance."""
    
    def __init__(self):
        # Initialize your chatbot service
        self.gemini_client = None
        self.anthropic_client = None
        self.openai_client = None
        
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_client = genai.GenerativeModel(settings.gemini_model)
        
        if settings.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        
        if settings.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=settings.openai_api_key)
        
        self.chat_collection = get_async_mongo_collection("chat_sessions")
        self.symptom_collection = get_async_mongo_collection("symptom_analyses")
    
    async def process_chat_message(self, message: str, user_id: str, session_id: Optional[str] = None) -> ChatResponse:
        """Process a chat message and return a response."""
        try:
            # Get or create session
            if not session_id:
                session_id = await self._create_chat_session(user_id)
            
            # Store user message
            await self._store_message(session_id, "user", message, user_id)
            
            # Analyze message for medical content
            medical_analysis = await self._analyze_medical_content(message, user_id)
            
            # Generate response based on analysis
            if medical_analysis.get("is_medical"):
                response = await self._generate_medical_response(message, medical_analysis, user_id)
            else:
                response = await self._generate_general_response(message, user_id)
            
            # Store bot response
            await self._store_message(session_id, "assistant", response, user_id)
            
            return ChatResponse(
                message=response,
                session_id=session_id,
                timestamp=datetime.utcnow(),
                is_medical=medical_analysis.get("is_medical", False),
                confidence=medical_analysis.get("confidence", 0.0)
            )
            
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return ChatResponse(
                message="I'm sorry, I'm having trouble processing your request. Please try again later.",
                session_id=session_id or "error",
                timestamp=datetime.utcnow(),
                is_medical=False,
                confidence=0.0
            )
    
    async def analyze_symptoms(self, symptoms_data: Dict[str, Any], user_id: str) -> SymptomAnalysisResponse:
        """Analyze symptoms using MCP and medical knowledge."""
        try:
            # Store symptom analysis request
            analysis_id = await self._store_symptom_analysis(symptoms_data, user_id)
            
            # Generate analysis using MCP
            analysis = await self._generate_symptom_analysis(symptoms_data)
            
            # Store results
            await self._update_symptom_analysis(analysis_id, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing symptoms: {str(e)}")
            return self._get_default_symptom_response()
    
    async def _create_chat_session(self, user_id: str) -> str:
        """Create a new chat session."""
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "messages": [],
            "is_active": True
        }
        result = await self.chat_collection.insert_one(session_data)
        return str(result.inserted_id)
    
    async def _store_message(self, session_id: str, role: str, content: str, user_id: str):
        """Store a message in the chat session."""
        message_data = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "user_id": user_id
        }
        
        await self.chat_collection.update_one(
            {"_id": session_id},
            {"$push": {"messages": message_data}, "$set": {"updated_at": datetime.utcnow()}}
        )
    
    async def _analyze_medical_content(self, message: str, user_id: str) -> Dict[str, Any]:
        """Analyze if the message contains medical content."""
        try:
            if self.gemini_client:
                response = await self._call_gemini_medical_analysis(message)
            elif self.anthropic_client:
                response = await self._call_anthropic_medical_analysis(message)
            elif self.openai_client:
                response = await self._call_openai_medical_analysis(message)
            else:
                return {"is_medical": False, "confidence": 0.0}
            
            return response
        except Exception as e:
            logger.error(f"Error analyzing medical content: {str(e)}")
            return {"is_medical": False, "confidence": 0.0}
    
    async def _call_gemini_medical_analysis(self, message: str) -> Dict[str, Any]:
        """Use Google Gemini for medical content analysis."""
        prompt = f"""
        Analyze the following message to determine if it contains medical content, symptoms, or health-related questions.
        
        Message: "{message}"
        
        Respond with a JSON object containing:
        - is_medical: boolean (true if medical content detected)
        - confidence: float (0.0 to 1.0)
        - detected_symptoms: array of strings (if any symptoms detected)
        - urgency_level: string (low, medium, high, emergency)
        - medical_categories: array of strings (e.g., ["symptoms", "medication", "diagnosis"])
        """
        
        try:
            response = self.gemini_client.generate_content(prompt)
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"is_medical": False, "confidence": 0.0}
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return {"is_medical": False, "confidence": 0.0}
    
    async def _call_anthropic_medical_analysis(self, message: str) -> Dict[str, Any]:
        """Use Anthropic Claude for medical content analysis."""
        prompt = f"""
        Analyze the following message to determine if it contains medical content, symptoms, or health-related questions.
        
        Message: "{message}"
        
        Respond with a JSON object containing:
        - is_medical: boolean (true if medical content detected)
        - confidence: float (0.0 to 1.0)
        - detected_symptoms: array of strings (if any symptoms detected)
        - urgency_level: string (low, medium, high, emergency)
        - medical_categories: array of strings (e.g., ["symptoms", "medication", "diagnosis"])
        """
        
        response = self.anthropic_client.messages.create(
            model=settings.mcp_model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"is_medical": False, "confidence": 0.0}
    
    async def _call_openai_medical_analysis(self, message: str) -> Dict[str, Any]:
        """Use OpenAI for medical content analysis."""
        prompt = f"""
        Analyze the following message to determine if it contains medical content, symptoms, or health-related questions.
        
        Message: "{message}"
        
        Respond with a JSON object containing:
        - is_medical: boolean (true if medical content detected)
        - confidence: float (0.0 to 1.0)
        - detected_symptoms: array of strings (if any symptoms detected)
        - urgency_level: string (low, medium, high, emergency)
        - medical_categories: array of strings (e.g., ["symptoms", "medication", "diagnosis"])
        """
        
        response = self.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"is_medical": False, "confidence": 0.0}
    
    async def _generate_medical_response(self, message: str, analysis: Dict[str, Any], user_id: str) -> str:
        """Generate a medical response using MCP."""
        try:
            if self.gemini_client:
                return await self._call_gemini_medical_response(message, analysis)
            elif self.anthropic_client:
                return await self._call_anthropic_medical_response(message, analysis)
            elif self.openai_client:
                return await self._call_openai_medical_response(message, analysis)
            else:
                return self._get_default_medical_response()
        except Exception as e:
            logger.error(f"Error generating medical response: {str(e)}")
            return self._get_default_medical_response()
    
    async def _call_gemini_medical_response(self, message: str, analysis: Dict[str, Any]) -> str:
        """Generate medical response using Google Gemini."""
        symptoms = analysis.get("detected_symptoms", [])
        urgency = analysis.get("urgency_level", "medium")
        
        prompt = f"""
        You are a medical AI assistant. Respond to the following health-related message with empathy and helpful guidance.
        
        Message: "{message}"
        Detected symptoms: {', '.join(symptoms) if symptoms else 'None'}
        Urgency level: {urgency}
        
        Guidelines:
        1. Be empathetic and understanding
        2. Provide helpful general health information
        3. Always recommend consulting healthcare professionals for serious concerns
        4. If urgency is high or emergency, emphasize seeking immediate medical attention
        5. Keep response concise but informative
        6. Include appropriate disclaimers about not replacing professional medical advice
        
        Response should be 2-3 sentences maximum.
        """
        
        try:
            response = self.gemini_client.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return self._get_default_medical_response()
    
    async def _call_anthropic_medical_response(self, message: str, analysis: Dict[str, Any]) -> str:
        """Generate medical response using Anthropic Claude."""
        symptoms = analysis.get("detected_symptoms", [])
        urgency = analysis.get("urgency_level", "medium")
        
        prompt = f"""
        You are a medical AI assistant. Respond to the following health-related message with empathy and helpful guidance.
        
        Message: "{message}"
        Detected symptoms: {', '.join(symptoms) if symptoms else 'None'}
        Urgency level: {urgency}
        
        Guidelines:
        1. Be empathetic and understanding
        2. Provide helpful general health information
        3. Always recommend consulting healthcare professionals for serious concerns
        4. If urgency is high or emergency, emphasize seeking immediate medical attention
        5. Keep response concise but informative
        6. Include appropriate disclaimers about not replacing professional medical advice
        
        Response should be 2-3 sentences maximum.
        """
        
        response = self.anthropic_client.messages.create(
            model=settings.mcp_model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _call_openai_medical_response(self, message: str, analysis: Dict[str, Any]) -> str:
        """Generate medical response using OpenAI."""
        symptoms = analysis.get("detected_symptoms", [])
        urgency = analysis.get("urgency_level", "medium")
        
        prompt = f"""
        You are a medical AI assistant. Respond to the following health-related message with empathy and helpful guidance.
        
        Message: "{message}"
        Detected symptoms: {', '.join(symptoms) if symptoms else 'None'}
        Urgency level: {urgency}
        
        Guidelines:
        1. Be empathetic and understanding
        2. Provide helpful general health information
        3. Always recommend consulting healthcare professionals for serious concerns
        4. If urgency is high or emergency, emphasize seeking immediate medical attention
        5. Keep response concise but informative
        6. Include appropriate disclaimers about not replacing professional medical advice
        
        Response should be 2-3 sentences maximum.
        """
        
        response = self.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def _generate_general_response(self, message: str, user_id: str) -> str:
        """Generate a general non-medical response."""
        return "I'm here to help with your health-related questions. Please feel free to ask me about symptoms, general health information, or any medical concerns you might have. Remember, I'm not a substitute for professional medical advice, so always consult with healthcare providers for serious concerns."
    
    async def _generate_symptom_analysis(self, symptoms_data: Dict[str, Any]) -> SymptomAnalysisResponse:
        """Generate comprehensive symptom analysis using MCP."""
        try:
            if self.gemini_client:
                return await self._call_gemini_symptom_analysis(symptoms_data)
            elif self.anthropic_client:
                return await self._call_anthropic_symptom_analysis(symptoms_data)
            elif self.openai_client:
                return await self._call_openai_symptom_analysis(symptoms_data)
            else:
                return self._get_default_symptom_response()
        except Exception as e:
            logger.error(f"Error generating symptom analysis: {str(e)}")
            return self._get_default_symptom_response()
    
    async def _call_gemini_symptom_analysis(self, symptoms_data: Dict[str, Any]) -> SymptomAnalysisResponse:
        """Generate symptom analysis using Google Gemini."""
        symptoms = symptoms_data.get("symptoms", [])
        age = symptoms_data.get("age")
        gender = symptoms_data.get("gender")
        medical_history = symptoms_data.get("medical_history", [])
        
        prompt = f"""
        Analyze the following symptoms and provide a structured medical assessment.
        
        Patient Information:
        - Age: {age if age else 'Not specified'}
        - Gender: {gender if gender else 'Not specified'}
        - Symptoms: {', '.join(symptoms)}
        - Medical History: {', '.join(medical_history) if medical_history else 'None'}
        
        Provide a JSON response with this structure:
        {{
            "conditions": [
                {{
                    "name": "Condition Name",
                    "probability": 0.85,
                    "description": "Brief description",
                    "severity": "mild|moderate|severe"
                }}
            ],
            "triage_advice": {{
                "urgency": "low|medium|high|emergency",
                "recommendation": "Specific recommendation",
                "timeframe": "When to seek care"
            }},
            "disclaimer": "Medical disclaimer",
            "confidence_score": 0.75,
            "follow_up_recommendations": ["Action 1", "Action 2"]
        }}
        
        Be conservative and always recommend professional medical consultation.
        """
        
        try:
            response = self.gemini_client.generate_content(prompt)
            data = json.loads(response.text)
            return self._parse_symptom_response(data)
        except json.JSONDecodeError:
            return self._get_default_symptom_response()
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return self._get_default_symptom_response()
    
    async def _call_anthropic_symptom_analysis(self, symptoms_data: Dict[str, Any]) -> SymptomAnalysisResponse:
        """Generate symptom analysis using Anthropic Claude."""
        symptoms = symptoms_data.get("symptoms", [])
        age = symptoms_data.get("age")
        gender = symptoms_data.get("gender")
        medical_history = symptoms_data.get("medical_history", [])
        
        prompt = f"""
        Analyze the following symptoms and provide a structured medical assessment.
        
        Patient Information:
        - Age: {age if age else 'Not specified'}
        - Gender: {gender if gender else 'Not specified'}
        - Symptoms: {', '.join(symptoms)}
        - Medical History: {', '.join(medical_history) if medical_history else 'None'}
        
        Provide a JSON response with this structure:
        {{
            "conditions": [
                {{
                    "name": "Condition Name",
                    "probability": 0.85,
                    "description": "Brief description",
                    "severity": "mild|moderate|severe"
                }}
            ],
            "triage_advice": {{
                "urgency": "low|medium|high|emergency",
                "recommendation": "Specific recommendation",
                "timeframe": "When to seek care"
            }},
            "disclaimer": "Medical disclaimer",
            "confidence_score": 0.75,
            "follow_up_recommendations": ["Action 1", "Action 2"]
        }}
        
        Be conservative and always recommend professional medical consultation.
        """
        
        response = self.anthropic_client.messages.create(
            model=settings.mcp_model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            data = json.loads(response.content[0].text)
            return self._parse_symptom_response(data)
        except json.JSONDecodeError:
            return self._get_default_symptom_response()
    
    async def _call_openai_symptom_analysis(self, symptoms_data: Dict[str, Any]) -> SymptomAnalysisResponse:
        """Generate symptom analysis using OpenAI."""
        symptoms = symptoms_data.get("symptoms", [])
        age = symptoms_data.get("age")
        gender = symptoms_data.get("gender")
        medical_history = symptoms_data.get("medical_history", [])
        
        prompt = f"""
        Analyze the following symptoms and provide a structured medical assessment.
        
        Patient Information:
        - Age: {age if age else 'Not specified'}
        - Gender: {gender if gender else 'Not specified'}
        - Symptoms: {', '.join(symptoms)}
        - Medical History: {', '.join(medical_history) if medical_history else 'None'}
        
        Provide a JSON response with this structure:
        {{
            "conditions": [
                {{
                    "name": "Condition Name",
                    "probability": 0.85,
                    "description": "Brief description",
                    "severity": "mild|moderate|severe"
                }}
            ],
            "triage_advice": {{
                "urgency": "low|medium|high|emergency",
                "recommendation": "Specific recommendation",
                "timeframe": "When to seek care"
            }},
            "disclaimer": "Medical disclaimer",
            "confidence_score": 0.75,
            "follow_up_recommendations": ["Action 1", "Action 2"]
        }}
        
        Be conservative and always recommend professional medical consultation.
        """
        
        response = self.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        
        try:
            data = json.loads(response.choices[0].message.content)
            return self._parse_symptom_response(data)
        except json.JSONDecodeError:
            return self._get_default_symptom_response()
    
    def _parse_symptom_response(self, data: Dict[str, Any]) -> SymptomAnalysisResponse:
        """Parse AI response into SymptomAnalysisResponse."""
        try:
            conditions = [
                Condition(
                    name=cond["name"],
                    probability=cond["probability"],
                    description=cond["description"],
                    severity=cond["severity"]
                )
                for cond in data.get("conditions", [])
            ]
            
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
            logger.error(f"Error parsing symptom response: {str(e)}")
            return self._get_default_symptom_response()
    
    def _get_default_symptom_response(self) -> SymptomAnalysisResponse:
        """Return a safe default symptom response."""
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
    
    def _get_default_medical_response(self) -> str:
        """Return a safe default medical response."""
        return "I understand you have health concerns. While I can provide general information, it's important to consult with a healthcare professional for proper medical advice and diagnosis."
    
    async def _store_symptom_analysis(self, symptoms_data: Dict[str, Any], user_id: str) -> str:
        """Store symptom analysis request."""
        analysis_data = {
            "user_id": user_id,
            "symptoms_data": symptoms_data,
            "created_at": datetime.utcnow(),
            "status": "pending"
        }
        result = await self.symptom_collection.insert_one(analysis_data)
        return str(result.inserted_id)
    
    async def _update_symptom_analysis(self, analysis_id: str, analysis: SymptomAnalysisResponse):
        """Update symptom analysis with results."""
        await self.symptom_collection.update_one(
            {"_id": analysis_id},
            {
                "$set": {
                    "analysis": analysis.dict(),
                    "status": "completed",
                    "updated_at": datetime.utcnow()
                }
            }
        )


# Global MCP chatbot service instance
mcp_chatbot = MCPChatbotService()
