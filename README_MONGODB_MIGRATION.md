# Healthify - MongoDB Migration & MCP Chatbot Integration

This document describes the migration from Redis/Docker to MongoDB and the integration of MCP (Model Context Protocol) chatbot for medical assistance.

## 🚀 What's New

### ✅ Completed Changes

1. **Removed Docker Dependencies**
   - Deleted `docker-compose.yml`
   - Deleted `Dockerfile`
   - Removed monitoring directory (Prometheus/Grafana)

2. **Migrated to MongoDB**
   - Replaced Redis with MongoDB for caching
   - Updated all database operations to use MongoDB
   - Created MongoDB setup script (`setup_mongodb.py`)
   - Updated Celery to use MongoDB as broker and backend

3. **Integrated MCP Chatbot**
   - Added MCP (Model Context Protocol) support
   - Created advanced medical chatbot service (`mcp_chatbot.py`)
   - Supports both Anthropic Claude and OpenAI models
   - Enhanced symptom analysis and medical assistance
   - Updated frontend to work with MCP chatbot

4. **Updated Dependencies**
   - Added MCP and Anthropic dependencies
   - Removed Redis dependencies
   - Updated requirements.txt

## 🛠️ Setup Instructions

### Prerequisites

1. **MongoDB** - Install and run MongoDB locally
   ```bash
   # Windows
   mongod --dbpath C:\data\db
   
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

2. **Python 3.11+** - Ensure you have Python 3.11 or higher

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   Create a `.env` file in the backend directory:
   ```env
   # MongoDB
   MONGO_URL=mongodb://localhost:27017/healthify
   MONGO_DATABASE=healthify
   
   # AI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # Security
   SECRET_KEY=your-super-secret-key-change-in-production
   
   # Environment
   ENVIRONMENT=development
   DEBUG=true
   ```

3. **Start the Backend**
   ```bash
   cd backend
   python start.py
   ```
   
   Or manually:
   ```bash
   python setup_mongodb.py  # Set up MongoDB
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the Frontend**
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### MongoDB Collections

The following collections are automatically created:
- `users` - User accounts and profiles
- `chat_sessions` - Chat session data
- `symptom_analyses` - Symptom analysis results
- `cache` - Application cache (with TTL)
- `audit_logs` - System audit logs
- `patients` - Patient records
- `medical_records` - Medical history
- `appointments` - Appointment scheduling
- `content` - Medical content and articles

### MCP Chatbot Features

1. **Medical Content Detection**
   - Automatically detects medical questions
   - Provides confidence scores
   - Shows medical disclaimers

2. **Symptom Analysis**
   - Advanced symptom analysis using MCP
   - Triage recommendations
   - Condition probability assessment

3. **Multi-Model Support**
   - Anthropic Claude (primary)
   - OpenAI GPT models (fallback)
   - Configurable model selection

## 🚨 Important Notes

### Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **MongoDB**: Ensure MongoDB is properly secured in production
3. **CORS**: Update CORS settings for production domains

### Medical Disclaimer

⚠️ **IMPORTANT**: This system is for informational purposes only and should not replace professional medical advice. Always consult healthcare professionals for medical concerns.

### Production Deployment

For production deployment:

1. **MongoDB**: Use MongoDB Atlas or a managed MongoDB service
2. **Environment**: Set `ENVIRONMENT=production` and `DEBUG=false`
3. **Security**: Use strong, unique secret keys
4. **Monitoring**: Implement proper logging and monitoring
5. **SSL**: Use HTTPS in production

## 🔍 API Endpoints

### Chat Endpoints

- `POST /api/chat/session` - Create new chat session
- `GET /api/chat/sessions` - Get user's chat sessions
- `GET /api/chat/sessions/{session_id}` - Get specific session
- `POST /api/chat/sessions/{session_id}/messages` - Send message
- `DELETE /api/chat/sessions/{session_id}` - End session
- `POST /api/chat/symptom` - Analyze symptoms

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - User logout

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Ensure MongoDB is running
   - Check connection string in `.env`
   - Verify MongoDB port (default: 27017)

2. **API Key Errors**
   - Verify API keys are set in `.env`
   - Check API key validity
   - Ensure sufficient API credits

3. **Frontend Connection Issues**
   - Check backend is running on port 8000
   - Verify CORS settings
   - Check browser console for errors

### Logs

Check logs for detailed error information:
- Backend: Console output or log files
- MongoDB: MongoDB log files
- Frontend: Browser developer console

## 📞 Support

For issues or questions:
1. Check this README
2. Review error logs
3. Check MongoDB and API key configurations
4. Ensure all dependencies are installed correctly

## 🔄 Migration Notes

### From Redis to MongoDB

- Cache operations now use MongoDB collections
- TTL is handled by MongoDB TTL indexes
- Session storage moved to MongoDB
- Celery broker/backend now uses MongoDB

### From Docker to Local

- No more Docker containers
- Direct MongoDB connection
- Local development setup
- Simplified deployment process

---

**Happy coding! 🎉**
