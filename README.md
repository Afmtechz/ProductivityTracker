# 🎯 ProductivityTracker - Gamified Productivity & Habit Tracking System

A modern, production-ready Python application for tracking tasks, habits, and productivity with gamification features, real-time updates, and a responsive web dashboard.

## ✨ Features

### Core Functionality
- ✅ **User Authentication** - Google OAuth 2.0 & Email/Password signup
- ✅ **Task Management** - CRUD operations with priorities, recurrence, and categories
- ✅ **Habit Tracking** - Daily habits with streak counters and heatmap analytics
- ✅ **Timetable Scheduler** - Schedule-based task management
- ✅ **Progress Analytics** - Daily/weekly completion statistics
- ✅ **Gamification** - XP system, achievements, levels, and streaks
- ✅ **Notifications & Reminders** - WebSocket real-time updates
- ✅ **Dark Mode** - Beautiful glassmorphism UI
- ✅ **Mobile Responsive** - PWA support for Android installation

### Dashboard Features
- 📊 Circular progress indicators
- 📈 Weekly heatmaps
- 📉 Productivity charts
- 🎮 Gamification leaderboards
- 🏆 Achievement badges
- ⚡ Real-time WebSocket updates

## 🏗️ Project Structure

```
ProductivityTracker/
├── backend/
│   ├── app/
│   │   ├── auth/              # Authentication & OAuth
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── jwt_handler.py
│   │   │   ├── google_oauth.py
│   │   │   └── router.py
│   │   │
│   │   ├── tasks/             # Task management
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   │
│   │   ├── habits/            # Habit tracking
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   │
│   │   ├── gamification/      # XP, levels, achievements
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   │
│   │   ├── utils/             # Utilities
│   │   │   ├── constants.py
│   │   │   ├── helpers.py
│   │   │   └── validators.py
│   │   │
│   │   ├── config.py          # Settings
│   │   ├── database.py        # DB setup
│   │   ├── dependencies.py    # Dependency injection
│   │   └── main.py            # FastAPI app entry
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── main.py
│
├── frontend/
│   ├── app.py                 # NiceGUI entry point
│   ├── pages/                 # NiceGUI pages
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── tasks.py
│   │   ├── habits.py
│   │   └── gamification.py
│   │
│   ├── components/            # Reusable UI components
│   └── assets/                # Static files
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── docs/
    ├── API.md
    ├── DEPLOYMENT.md
    └── ARCHITECTURE.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Afmtechz/ProductivityTracker.git
   cd ProductivityTracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the backend**
   ```bash
   python backend/main.py
   # Or with uvicorn directly:
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Start the frontend** (in another terminal)
   ```bash
   cd frontend
   python app.py
   ```

Access the application at `http://localhost:8000`

## 🔐 Authentication

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable OAuth 2.0
4. Create OAuth credentials (Web application)
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback`
   - `https://yourdomain.com/auth/google/callback`
6. Copy Client ID and Secret to `.env`

### API Endpoints

#### Authentication
```bash
# Register with email/password
POST /auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}

# Login
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}

# Google OAuth login
POST /auth/google
{
  "token": "google_id_token"
}

# Refresh token
POST /auth/refresh
{
  "refresh_token": "your_refresh_token"
}

# Get OAuth URL
GET /auth/google/url
```

#### Tasks
```bash
# List tasks
GET /tasks?skip=0&limit=10&category=work&priority=high

# Create task
POST /tasks
{
  "title": "Complete project",
  "description": "Finish the feature",
  "priority": "high",
  "category": "work",
  "due_date": "2026-05-25",
  "estimated_duration": 120,
  "is_recurring": true,
  "recurrence_type": "daily"
}

# Update task
PUT /tasks/{task_id}

# Mark task as complete
POST /tasks/{task_id}/complete

# Delete task
DELETE /tasks/{task_id}

# Get daily stats
GET /tasks/stats/daily?date=2026-05-19

# Get weekly stats
GET /tasks/stats/weekly?date=2026-05-19
```

#### Habits
```bash
# List habits
GET /habits

# Create habit
POST /habits
{
  "name": "Morning Exercise",
  "description": "30 mins cardio",
  "frequency": "daily",
  "color": "#FF6B6B",
  "goal_date": "2026-12-31"
}

# Log habit completion
POST /habits/{habit_id}/log

# Get weekly heatmap
GET /habits/{habit_id}/heatmap?week_offset=0

# Get habit stats
GET /habits/{habit_id}/stats
```

#### Gamification
```bash
# Get user profile with XP/levels
GET /users/me

# Get achievements
GET /gamification/achievements

# Get leaderboard
GET /gamification/leaderboard?limit=10
```

## 🎮 Gamification System

### XP Rewards
- Task completion: 50 XP (base) × priority multiplier
- Habit completion: 30 XP
- Streak bonuses: 1.5x multiplier
- Achievement unlocks: 100-500 XP bonus

### Achievements
🎯 **First Steps** - Complete your first task
👑 **Task Master** - Complete 50 tasks
🥷 **Productivity Ninja** - Achieve 95% completion rate
⚔️ **Week Warrior** - Maintain a 7-day streak
🏆 **Habit Master** - Achieve a 30-day streak
👑 **Streak King** - Achieve a 100-day streak

### Levels
Progressive levels based on cumulative XP:
- Level 1-10: 1,000 XP per level
- Level 11-20: 2,000 XP per level
- Level 21+: 3,000 XP per level

## 📱 PWA & Mobile Support

The application includes:
- `manifest.json` - PWA manifest for app installation
- Service worker - Offline support
- Responsive design - Mobile-first UI
- Android installation - Add to home screen

## 🐳 Docker Deployment

```bash
# Build image
docker build -t productivity-tracker .

# Run container
docker run -p 8000:8000 --env-file .env productivity-tracker

# Using docker-compose
docker-compose up -d
```

## 📊 Database Setup

### SQLite (Development)
Default configuration. Database file: `test.db`

### PostgreSQL (Production)
Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/productivity_tracker
```

## 🔄 WebSocket Real-time Updates

Connect to WebSocket for live notifications:
```python
ws://localhost:8000/ws/{user_id}
```

Events:
- `task_completed` - Task completion notification
- `habit_logged` - Habit logged
- `achievement_unlocked` - New achievement
- `level_up` - User leveled up

## 📈 Analytics & Reports

- Daily completion percentage
- Weekly trend analysis
- Habit consistency heatmaps
- Productivity scores
- Streak analytics
- Achievement progress

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with SQLite/PostgreSQL support
- **Pydantic** - Data validation
- **Python-Jose** - JWT token handling
- **Google Auth** - OAuth 2.0 integration
- **APScheduler** - Task scheduling
- **WebSockets** - Real-time updates

### Frontend
- **NiceGUI** - Python web UI framework
- **Tailwind CSS** - Responsive styling
- **Chart.js** - Analytics visualization
- **PWA** - Progressive web app

### Database
- **SQLite** - Development
- **PostgreSQL** - Production
- **Alembic** - Migrations

## 🔒 Security Best Practices

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ CORS configuration
- ✅ Environment variables for secrets
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (ORM)
- ✅ HTTPS in production

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Architecture Overview](docs/ARCHITECTURE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙋 Support

For issues, questions, or suggestions:
- Create an [Issue](https://github.com/Afmtechz/ProductivityTracker/issues)
- Check [Discussions](https://github.com/Afmtechz/ProductivityTracker/discussions)
- Email: support@productivitytracker.dev

## 🎉 Acknowledgments

Built with ❤️ using FastAPI, NiceGUI, and SQLAlchemy
