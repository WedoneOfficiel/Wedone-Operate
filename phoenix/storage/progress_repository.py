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
    def class_report(self, class_id: str, teacher_id: str) -> list[dict]:
        """Return a teacher-scoped, question-weighted report for every active student."""
        with self.database.connect() as connection:
            classroom = connection.execute(
                "SELECT name, school_year FROM classes "
                "WHERE id=? AND owner_teacher_id=? AND archived_at IS NULL",
                (class_id, teacher_id),
            ).fetchone()
            if classroom is None:
                raise ValueError("Classe introuvable dans votre espace professeur.")
            rows = connection.execute(
                """SELECT st.id, st.display_name,
                          COALESCE(g.name, '') AS group_name,
                          COUNT(DISTINCT ps.id) AS sessions,
                          COUNT(pa.id) AS answered,
                          COALESCE(SUM(pa.is_correct), 0) AS correct,
                          COALESCE(SUM(pa.elapsed_ms), 0) AS elapsed_ms
                   FROM students st
                   LEFT JOIN groups g ON g.id=st.group_id
                   LEFT JOIN practice_sessions ps
                     ON ps.student_id=st.id AND ps.mode='classroom'
                   LEFT JOIN practice_answers pa ON pa.session_id=ps.id
                   WHERE st.class_id=? AND st.archived_at IS NULL
                   GROUP BY st.id
                   ORDER BY st.display_name COLLATE NOCASE""",
                (class_id,),
            ).fetchall()
        report = []
        for row in rows:
            item = dict(row)
            item["student_id"] = item.pop("id")
            item["class_name"] = classroom["name"]
            item["school_year"] = classroom["school_year"] or ""
            item["accuracy"] = (
                round(item["correct"] / item["answered"] * 100, 1)
                if item["answered"] else None
            )
            report.append(item)
        return report

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
