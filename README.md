# Study Tracker API

A Flask-based REST API for tracking study sessions.

## Features

- Create study sessions with topic, start time, end time, and notes
- View all study sessions
- View individual study sessions
- Automatic duration calculation
- Input validation and error handling

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
SECRET_KEY=your_secret_key
```

4. Run the application:
```bash
python run.py
```

## API Endpoints

### Create Study Session
- **POST** `/api/v1/sessions`
- **Body**:
```json
{
    "topic": "Mathematics",
    "start_time": "2024-02-20 14:00",
    "end_time": "2024-02-20 15:30",
    "notes": "Studied calculus"
}
```

### Get All Study Sessions
- **GET** `/api/v1/sessions`

### Get Specific Study Session
- **GET** `/api/v1/sessions/<session_id>`

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`

## TODO

- [ ] Implement user authentication
- [ ] Add session update and delete endpoints
- [ ] Add pagination for GET endpoints
- [ ] Add filtering and sorting options
- [ ] Add more comprehensive error handling
- [ ] Add API documentation with Swagger/OpenAPI 