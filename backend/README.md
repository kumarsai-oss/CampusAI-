# CampusAI Backend

Comprehensive Campus Management System with AI Integration using FastAPI and PostgreSQL.

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Student Management**: CRUD operations, academic tracking, performance prediction
- **Faculty Management**: Staff profiles, department management
- **Attendance System**: Face recognition integration, attendance tracking
- **Timetable Management**: Class scheduling with optimization using OR-Tools
- **Results & Grades**: Student performance tracking, GPA calculations
- **Fee Management**: Tuition fee tracking and payment status
- **Placements**: Placement drive management, resume ATS analysis
- **Notices**: Campus notifications with AI summarization
- **Complaints**: Student complaint portal with resolution tracking
- **AI Integration**: Gemini API for chatbot, summarization, and analysis

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Face Recognition**: face_recognition library
- **Optimization**: Google OR-Tools
- **ML**: scikit-learn
- **AI**: Google Gemini API

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or poetry

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kumarsai-oss/CampusAI-.git
   cd backend
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

5. **Initialize database**
   ```bash
   python init_db.py
   ```
   
   This will:
   - Create all database tables
   - Create default admin user (username: admin, password: admin123456)

6. **Run the server**
   ```bash
   python run.py
   ```
   
   Server will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/api/docs`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/change-password` - Change password

### Student Management
- `POST /api/students/` - Create student
- `GET /api/students/` - List students
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student
- `GET /api/students/{id}/academic-history` - Get academic history

### Faculty Management
- `POST /api/faculty/` - Create faculty
- `GET /api/faculty/` - List faculty
- `GET /api/faculty/{id}` - Get faculty details
- `PUT /api/faculty/{id}` - Update faculty
- `DELETE /api/faculty/{id}` - Delete faculty

### Attendance
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/student/{id}` - Get student attendance
- `GET /api/attendance/report/{id}` - Get attendance report
- `PUT /api/attendance/{id}` - Update attendance

### Results
- `POST /api/results/` - Create result
- `GET /api/results/student/{id}` - Get student results
- `PUT /api/results/{id}` - Update result
- `POST /api/results/subjects` - Create subject
- `GET /api/results/subjects` - List subjects

### Fees
- `POST /api/fees/` - Create fee record
- `GET /api/fees/student/{id}` - Get student fees
- `PUT /api/fees/{id}` - Update fee
- `GET /api/fees/` - List all fees

### Timetable
- `POST /api/timetable/` - Create timetable
- `GET /api/timetable/` - List timetables
- `GET /api/timetable/{id}` - Get timetable
- `POST /api/timetable/slots` - Add time slot
- `POST /api/timetable/optimize` - Optimize timetable

### Placements
- `POST /api/placements/drives` - Create placement drive
- `GET /api/placements/drives` - List placement drives
- `POST /api/placements/` - Create placement
- `GET /api/placements/student/{id}` - Get student placement
- `PUT /api/placements/{id}` - Update placement
- `POST /api/placements/resume/analyze` - Analyze resume for ATS

### Notices
- `POST /api/notices/` - Create notice
- `GET /api/notices/` - List notices
- `GET /api/notices/{id}` - Get notice
- `PUT /api/notices/{id}` - Update notice
- `DELETE /api/notices/{id}` - Delete notice
- `POST /api/notices/summarize` - Summarize notice

### Complaints
- `POST /api/complaints/` - Create complaint
- `GET /api/complaints/` - List complaints
- `GET /api/complaints/{id}` - Get complaint
- `GET /api/complaints/student/{id}` - Get student complaints
- `PUT /api/complaints/{id}` - Update complaint

### AI Features
- `POST /api/ai/chat` - Chat with AI bot
- `POST /api/ai/summarize` - Summarize content
- `POST /api/ai/performance-prediction` - Predict student performance

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123456

**⚠️ IMPORTANT: Change these credentials in production!**

## Environment Variables

See `.env.example` for all available configuration options:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/campusai_db
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

## Project Structure

```
backend/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # API route handlers
│   ├── services/         # Business logic services
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   ├── security.py       # Authentication & authorization
│   └── main.py          # FastAPI application
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── init_db.py           # Database initialization
├── run.py               # Development server
└── README.md            # This file
```

## Database Models

- **User** - Authentication and authorization
- **Student** - Student information
- **StudentAcademic** - Academic records
- **Faculty** - Faculty information
- **Attendance** - Attendance records with face recognition
- **Timetable** - Class scheduling
- **TimeSlot** - Individual class slots
- **Result** - Student grades
- **Subject** - Course information
- **Fee** - Fee management
- **Placement** - Placement records
- **PlacementDrive** - Recruitment drives
- **Notice** - Campus notifications
- **Complaint** - Student complaints

## Testing

Use the interactive API documentation at `/api/docs` to test all endpoints.

## Performance Optimization

- Connection pooling for database
- Indexed queries for fast lookups
- Caching for frequently accessed data
- Async/await for non-blocking operations

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation with Pydantic
- CORS configuration
- SQL injection prevention with SQLAlchemy ORM

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.
