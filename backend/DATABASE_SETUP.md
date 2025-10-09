# 🗄️ Database Setup Guide for Healthify Backend

## Quick Setup (Recommended)

### Step 1: Install PostgreSQL
1. Download from: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set for `postgres` user

### Step 2: Create Database
Open Command Prompt or PowerShell and run:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE healthify;
CREATE USER healthify_user WITH PASSWORD 'healthify_password';
GRANT ALL PRIVILEGES ON DATABASE healthify TO healthify_user;
\q
```

### Step 3: Set Environment Variables
Create a `.env` file in the backend directory with:

```env
DATABASE_URL=postgresql://healthify_user:healthify_password@localhost:5432/healthify
SECRET_KEY=your-super-secret-key-change-in-production-12345
OPENAI_API_KEY=your-openai-api-key-here
```

### Step 4: Run Database Setup
```bash
py setup_database.py
```

### Step 5: Start the Server
```bash
py -m uvicorn app.main:app --reload
```

## Alternative: Use Docker (Easier)

If you have Docker installed:
```bash
docker-compose up -d
```

This will automatically set up PostgreSQL, Redis, and all services.

## Troubleshooting

### PostgreSQL not found
- Make sure PostgreSQL is installed and running
- Add PostgreSQL bin directory to your PATH
- Restart your terminal after installation

### Connection refused
- Check if PostgreSQL service is running
- Verify the database URL in .env file
- Make sure the database and user exist

### Permission denied
- Make sure the user has proper privileges
- Check the password is correct

## Verification

After setup, test the connection:
```bash
py -c "from app.database import engine; print('✅ Database connected!')"
```

## Next Steps

1. Start the server: `py -m uvicorn app.main:app --reload`
2. Access API docs: http://localhost:8000/docs
3. Test endpoints: http://localhost:8000/health
