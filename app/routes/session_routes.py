from flask import Blueprint, request, jsonify, g, send_file
from app.db import get_db_connection
from datetime import datetime
from typing import Dict, Any
import logging
import pandas as pd
import io

session_bp = Blueprint('sessions', __name__)

def validate_session_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate session data."""
    required_fields = ['topic', 'start_time', 'end_time']
    for field in required_fields:
        if not data.get(field):
            return False, f"Missing required field: {field}"
    
    try:
        start_dt = datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(data['end_time'], "%Y-%m-%d %H:%M")
        
        if end_dt <= start_dt:
            return False, "End time must be after start time"
            
        if (end_dt - start_dt).total_seconds() > 24 * 60 * 60:  # 24 hours
            return False, "Session duration cannot exceed 24 hours"
            
    except ValueError:
        return False, "Invalid datetime format. Use YYYY-MM-DD HH:MM"
    
    return True, ""

@session_bp.route('/sessions', methods=['POST'])
def create_session():
    """Create a new study session."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        is_valid, error_message = validate_session_data(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        start_dt = datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(data['end_time'], "%Y-%m-%d %H:%M")
        duration = int((end_dt - start_dt).total_seconds() / 60)
        notes = data.get('notes', '')
        
        # TODO: Replace with actual user authentication
        user_id = 1  # Temporary hardcoded user_id

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO study_sessions (user_id, topic, start_time, end_time, duration, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (user_id, data['topic'], start_dt, end_dt, duration, notes)
            )
            session_id = cursor.lastrowid

        return jsonify({
            "message": "Study session logged successfully",
            "session_id": session_id
        }), 201

    except Exception as e:
        logging.error(f"Error creating session: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@session_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all study sessions for the current user."""
    try:
        # TODO: Replace with actual user authentication
        user_id = 1  # Temporary hardcoded user_id
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM study_sessions 
                WHERE user_id = %s 
                ORDER BY start_time DESC
                """,
                (user_id,)
            )
            sessions = cursor.fetchall()

        return jsonify({"sessions": sessions}), 200

    except Exception as e:
        logging.error(f"Error fetching sessions: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@session_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific study session."""
    try:
        # TODO: Replace with actual user authentication
        user_id = 1  # Temporary hardcoded user_id
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM study_sessions 
                WHERE id = %s AND user_id = %s
                """,
                (session_id, user_id)
            )
            session = cursor.fetchone()

        if not session:
            return jsonify({"error": "Session not found"}), 404

        return jsonify({"session": session}), 200

    except Exception as e:
        logging.error(f"Error fetching session: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@session_bp.route('/sessions/export', methods=['GET'])
def export_sessions():
    """Export study sessions to Excel file."""
    try:
        # TODO: Replace with actual user authentication
        user_id = 1  # Temporary hardcoded user_id
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    id,
                    topic,
                    start_time,
                    end_time,
                    duration,
                    notes,
                    created_at
                FROM study_sessions 
                WHERE user_id = %s 
                ORDER BY start_time DESC
                """,
                (user_id,)
            )
            sessions = cursor.fetchall()

        if not sessions:
            return jsonify({"error": "No sessions found"}), 404

        # Convert to pandas DataFrame
        df = pd.DataFrame(sessions)
        
        # Format datetime columns
        df['start_time'] = pd.to_datetime(df['start_time']).dt.strftime('%Y-%m-%d %H:%M')
        df['end_time'] = pd.to_datetime(df['end_time']).dt.strftime('%Y-%m-%d %H:%M')
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Rename columns for better readability
        df = df.rename(columns={
            'id': 'Session ID',
            'topic': 'Topic',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'duration': 'Duration (minutes)',
            'notes': 'Notes',
            'created_at': 'Created At'
        })

        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Study Sessions', index=False)
            
            # Auto-adjust columns' width
            worksheet = writer.sheets['Study Sessions']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2

        output.seek(0)
        
        # Generate filename with current date
        filename = f"study_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logging.error(f"Error exporting sessions: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    
        
    