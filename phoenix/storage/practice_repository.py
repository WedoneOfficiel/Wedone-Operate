"""Persistence operations for individual and classroom practice sessions."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import sqlite3
from uuid import uuid4

from .database import Database


class PracticeRepository:
    def __init__(self, database: Database):
        self.database = database

    def start_session(
        self,
        mode: str,
        question_count: int,
        configuration: dict,
        student_id: str | None = None,
    ) -> str:
        if mode not in ("individual", "classroom"):
            raise ValueError("Mode de séance invalide.")
        if mode == "individual" and student_id is not None:
            raise ValueError("Une séance individuelle ne peut pas être liée à un élève.")
        if mode == "classroom" and not student_id:
            raise ValueError("Une séance en classe doit être liée à un élève.")
        if not 1 <= question_count <= 500:
            raise ValueError("Le nombre de questions doit être compris entre 1 et 500.")
        session_id = str(uuid4())
        started_at = datetime.now(timezone.utc).isoformat()
        payload = dict(configuration)
        payload["question_count"] = question_count
        with self.database.transaction() as connection:
            connection.execute(
                """INSERT INTO practice_sessions
                   (id, student_id, mode, status, configuration_json, started_at,
                    correct_count, question_count)
                   VALUES (?, ?, ?, 'in_progress', ?, ?, 0, ?)""",
                (session_id, student_id, mode, json.dumps(payload, ensure_ascii=False), started_at, question_count),
            )
        return session_id

    def record_answer(
        self,
        session_id: str,
        skill_id: str,
        prompt: str,
        expected_answer: int | str,
        given_answer: str | int,
        elapsed_ms: int | None = None,
    ) -> bool:
        if elapsed_ms is not None and elapsed_ms < 0:
            raise ValueError("Le temps de réponse ne peut pas être négatif.")
        expected = str(expected_answer).strip()
        given = str(given_answer).strip()
        try:
            is_correct = int(given) == int(expected)
        except ValueError:
            is_correct = False
        answer_id = str(uuid4())
        with self.database.transaction() as connection:
            session = connection.execute(
                "SELECT status, question_count FROM practice_sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
            if session is None:
                raise ValueError("Séance introuvable.")
            if session["status"] != "in_progress":
                raise ValueError("Cette séance n'accepte plus de réponses.")
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM practice_answers WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            position = int(row["count"])
            if position >= session["question_count"]:
                raise ValueError("Toutes les questions de cette séance ont déjà une réponse.")
            connection.execute(
                """INSERT INTO practice_answers
                   (id, session_id, position, skill_id, prompt, expected_answer,
                    given_answer, is_correct, elapsed_ms)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (answer_id, session_id, position, skill_id, prompt, expected, given,
                 int(is_correct), elapsed_ms),
            )
            connection.execute(
                """UPDATE practice_sessions
                   SET correct_count = correct_count + ?
                   WHERE id = ?""",
                (int(is_correct), session_id),
            )
        return is_correct

    def finish_session(self, session_id: str) -> dict:
        finished_at = datetime.now(timezone.utc).isoformat()
        with self.database.transaction() as connection:
            session = connection.execute(
                "SELECT status, question_count, correct_count FROM practice_sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
            if session is None:
                raise ValueError("Séance introuvable.")
            if session["status"] != "in_progress":
                raise ValueError("Cette séance est déjà terminée.")
            answered = connection.execute(
                "SELECT COUNT(*) FROM practice_answers WHERE session_id = ?",
                (session_id,),
            ).fetchone()[0]
            if answered != session["question_count"]:
                raise ValueError("Toutes les questions doivent être traitées avant de terminer la séance.")
            connection.execute(
                "UPDATE practice_sessions SET status='completed', finished_at=? WHERE id=?",
                (finished_at, session_id),
            )
            return {"status": "completed", "answered": answered, "correct": session["correct_count"]}

    def abandon_session(self, session_id: str) -> dict:
        finished_at = datetime.now(timezone.utc).isoformat()
        with self.database.transaction() as connection:
            session = connection.execute(
                "SELECT status, correct_count, question_count FROM practice_sessions WHERE id=?",
                (session_id,),
            ).fetchone()
            if session is None:
                raise ValueError("Séance introuvable.")
            if session["status"] != "in_progress":
                raise ValueError("Cette séance est déjà terminée.")
            answered = connection.execute(
                "SELECT COUNT(*) FROM practice_answers WHERE session_id=?",
                (session_id,),
            ).fetchone()[0]
            connection.execute(
                "UPDATE practice_sessions SET status='abandoned', finished_at=? WHERE id=?",
                (finished_at, session_id),
            )
            return {
                "status": "abandoned",
                "answered": answered,
                "question_count": session["question_count"],
                "correct": session["correct_count"],
            }

    def get_session(self, session_id: str) -> dict | None:
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT * FROM practice_sessions WHERE id=?", (session_id,)
            ).fetchone()
            if row is None:
                return None
            answers = connection.execute(
                "SELECT * FROM practice_answers WHERE session_id=? ORDER BY position",
                (session_id,),
            ).fetchall()
        result = dict(row)
        result["configuration"] = json.loads(result.pop("configuration_json"))
        result["answers"] = [dict(answer) for answer in answers]
        return result
