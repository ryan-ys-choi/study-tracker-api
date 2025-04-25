from flask import Blueprint, request, jsonify
from app.db import get_db
from datetime import datetime

session_bp = Blueprint('sessions', __name__)

# @blueprint.route() is used to bind a URL path to a Python function
@session_bp.route('/sessions', methods=['POST'])
def log_session():
    data = request.get_json() # Reads the JSON of the incoming request
    topic = data.get('topic')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    notes = data.get('notes', '') # it defaults to an empty string
    
    if not topic or not start_time or not end_time:
        return jsonify(message="Missing fields"), 400
    try:
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    except:
        return jsonify(message="Invalid data format"), 400
    
    # Calculate duration in minutes
    duration = int((end_dt - start_dt).total_seconds() / 60)
    user_id = 1
    
    # insert a new study session into MySQL database
    conn = get_db()
    cursor = conn.cursor() 
    cursor.execute(
        """
        INSERT INTO study_sessions (user_id, topic, start_time, end_time, duration, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, topic, start_dt, end_dt, duration, notes)
    )
    conn.commit()
    
    return jsonify(message="Study session logged successfully"), 201

    
        
    