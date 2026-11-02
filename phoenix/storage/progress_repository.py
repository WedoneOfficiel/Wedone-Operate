"""Question-weighted progress summaries for Phoenix practice history."""

from __future__ import annotations

from .database import Database


class ProgressRepository:
    def __init__(self, database: Database):
        self.database = database

    def overview(self, mode: str, student_id: str | None = None) -> dict:
        if mode not in ("individual", "classroom"):
            raise ValueError("Mode de progression invalide.")
        if mode == "individual" and student_id is not None:
            raise ValueError("La progression individuelle ne prend pas d'identifiant élève.")
        if mode == "classroom" and student_id is None:
            raise ValueError("Sélectionnez un élève pour consulter sa progression.")

        where = "s.mode=? AND s.student_id IS NULL" if mode == "individual" else "s.mode=? AND s.student_id=?"
        parameters = (mode,) if mode == "individual" else (mode, student_id)

        with self.database.connect() as connection:
            totals = connection.execute(
                f"""SELECT COUNT(DISTINCT s.id) AS sessions,
                           COUNT(DISTINCT CASE WHEN s.status='completed' THEN s.id END) AS completed,
                           COUNT(DISTINCT CASE WHEN s.status='abandoned' THEN s.id END) AS abandoned,
                           COUNT(a.id) AS answered,
                           COALESCE(SUM(a.is_correct), 0) AS correct,
                           COALESCE(SUM(a.elapsed_ms), 0) AS elapsed_ms
                    FROM practice_sessions s
                    LEFT JOIN practice_answers a ON a.session_id=s.id
                    WHERE {where}""",
                parameters,
            ).fetchone()
            recent = connection.execute(
                f"""SELECT s.id, s.started_at, s.status, s.question_count,
                           s.correct_count, COUNT(a.id) AS answered_count
                    FROM practice_sessions s
                    LEFT JOIN practice_answers a ON a.session_id=s.id
                    WHERE {where}
                    GROUP BY s.id
                    ORDER BY s.started_at DESC
                    LIMIT 8""",
                parameters,
            ).fetchall()
            skills = connection.execute(
                f"""SELECT a.skill_id, COUNT(*) AS answered,
                           COALESCE(SUM(a.is_correct), 0) AS correct,
                           AVG(a.elapsed_ms) AS average_elapsed_ms
                    FROM practice_sessions s
                    JOIN practice_answers a ON a.session_id=s.id
                    WHERE {where}
                    GROUP BY a.skill_id
                    ORDER BY answered DESC, a.skill_id""",
                parameters,
            ).fetchall()

        answered = int(totals["answered"] or 0)
        correct = int(totals["correct"] or 0)
        return {
            "sessions": int(totals["sessions"] or 0),
            "completed": int(totals["completed"] or 0),
            "abandoned": int(totals["abandoned"] or 0),
            "answered": answered,
            "correct": correct,
            "accuracy": round(correct / answered * 100, 1) if answered else None,
            "elapsed_ms": int(totals["elapsed_ms"] or 0),
            "recent": [dict(row) for row in recent],
            "skills": [
                {
                    "skill_id": row["skill_id"],
                    "answered": int(row["answered"]),
                    "correct": int(row["correct"]),
                    "accuracy": round(row["correct"] / row["answered"] * 100, 1),
                    "average_elapsed_ms": (
                        round(row["average_elapsed_ms"], 1)
                        if row["average_elapsed_ms"] is not None else None
                    ),
                }
                for row in skills
            ],
        }
