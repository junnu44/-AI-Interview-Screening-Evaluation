import sqlite3
import os
import datetime
from typing import Tuple, List, Any, Optional

# -------------------------------------------------------------
# ✅ Initialize DB
# -------------------------------------------------------------
def init_db(db_path: str):
    # Prevent crash when db_path has no folder
    folder = os.path.dirname(db_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS candidates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            role TEXT,
            experience TEXT,
            hobbies TEXT,
            resume_name TEXT,
            created_at TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS interviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            started_at TEXT,
            submitted_at TEXT,
            overall_score REAL,
            status TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS responses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id INTEGER,
            question_index INTEGER,
            category TEXT,
            question_text TEXT,
            transcript TEXT,
            ai_score REAL,
            ai_feedback TEXT,
            created_at TEXT
        )
        """)

        conn.commit()


# -------------------------------------------------------------
# ✅ Candidate save
# -------------------------------------------------------------
def save_candidate(full_name, email, role, experience, hobbies, resume_name, db_path) -> int:
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO candidates(full_name,email,role,experience,hobbies,resume_name,created_at)
            VALUES(?,?,?,?,?,?,?)
        """, (
            full_name, email, role, experience, hobbies,
            resume_name, datetime.datetime.utcnow().isoformat()
        ))
        cid = c.lastrowid
        conn.commit()
        return cid


# -------------------------------------------------------------
# ✅ Create interview record
# -------------------------------------------------------------
def create_interview(candidate_id, db_path) -> int:
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO interviews(candidate_id, started_at, status)
            VALUES(?,?,?)
        """, (
            candidate_id,
            datetime.datetime.utcnow().isoformat(),
            "IN_PROGRESS"
        ))
        iid = c.lastrowid
        conn.commit()
        return iid


# -------------------------------------------------------------
# ✅ Save response
# -------------------------------------------------------------
def save_response(interview_id, question_index, category, question_text,
                  transcript, score, feedback, db_path):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO responses(
                interview_id, question_index, category, question_text,
                transcript, ai_score, ai_feedback, created_at
            )
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            interview_id, question_index, category, question_text,
            transcript, score, feedback,
            datetime.datetime.utcnow().isoformat()
        ))
        conn.commit()


# -------------------------------------------------------------
# ✅ List candidates w/ interview summary
# -------------------------------------------------------------
def list_candidates(db_path) -> List[tuple]:
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT
                c.id,
                c.full_name,
                c.email,
                c.role,
                i.id AS interview_id,
                i.started_at,
                i.status,
                i.overall_score
            FROM candidates c
            LEFT JOIN interviews i ON i.candidate_id = c.id
            ORDER BY c.id DESC
        """)
        rows = c.fetchall()
        return rows


# -------------------------------------------------------------
# ✅ Get full candidate details + responses
# -------------------------------------------------------------
def get_candidate_details(candidate_id, db_path) -> Tuple[Optional[tuple], List[tuple]]:
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

        c.execute("SELECT * FROM candidates WHERE id=?", (candidate_id,))
        cand = c.fetchone()

        if not cand:
            return None, []

        # Get interview id for this candidate
        c.execute("SELECT id FROM interviews WHERE candidate_id=?", (candidate_id,))
        row = c.fetchone()
        if not row:
            return cand, []

        interview_id = row[0]

        # Fetch responses
        c.execute("""
            SELECT
                question_index,
                category,
                question_text,
                transcript,
                ai_score,
                ai_feedback,
                created_at
            FROM responses
            WHERE interview_id=?
            ORDER BY question_index
        """, (interview_id,))
        responses = c.fetchall()

        return cand, responses


# -------------------------------------------------------------
# ✅ FINALIZE INTERVIEW — Compute final score
# -------------------------------------------------------------
def finalize_interview(interview_id, db_path) -> float:
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

        c.execute("SELECT avg(ai_score) FROM responses WHERE interview_id=?", (interview_id,))
        avg_score = c.fetchone()[0] or 0

        c.execute("""
            UPDATE interviews
            SET submitted_at = ?, overall_score = ?, status = 'COMPLETED'
            WHERE id = ?
        """, (
            datetime.datetime.utcnow().isoformat(),
            avg_score,
            interview_id
        ))

        conn.commit()
        return float(avg_score)
