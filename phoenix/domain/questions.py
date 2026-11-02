"""Deterministic, testable question generation for mental arithmetic."""

from __future__ import annotations

from dataclasses import dataclass
import random

from .curriculum import Skill, get_skill


@dataclass(frozen=True)
class Question:
    skill_id: str
    prompt: str
    answer: int
    operands: tuple[int, int]
    operation: str

    @property
    def signature(self) -> tuple[str, int, int]:
        return (self.operation, self.operands[0], self.operands[1])


def _integer_question(skill: Skill, difficulty: int, rng: random.Random) -> Question:
    if not skill.enabled:
        raise ValueError(f"Cette compétence n'a pas encore de générateur : {skill.id}")
    if not 1 <= difficulty <= 5:
        raise ValueError("La difficulté doit être comprise entre 1 et 5.")

    operation = skill.operation
    if operation == "addition":
        limits = {1: 10, 2: 20, 3: 100, 4: 500, 5: 1000}
        maximum = limits[difficulty]
        a = rng.randint(0, maximum)
        b = rng.randint(0, maximum - a)
        answer = a + b
        symbol = "+"
    elif operation == "subtraction":
        limits = {1: 10, 2: 20, 3: 100, 4: 500, 5: 1000}
        maximum = limits[difficulty]
        a = rng.randint(0, maximum)
        b = rng.randint(0, a)
        answer = a - b
        symbol = "−"
    elif operation == "multiplication":
        if skill.id == "ce2.multiplication_tables":
            upper = min(10, 5 + difficulty)
            a, b = rng.randint(2, upper), rng.randint(2, upper)
        else:
            upper = {1: 5, 2: 10, 3: 20, 4: 50, 5: 100}[difficulty]
            a, b = rng.randint(2, upper), rng.randint(2, upper)
        answer = a * b
        symbol = "×"
    elif operation == "division":
        divisor_max = {1: 5, 2: 10, 3: 12, 4: 20, 5: 25}[difficulty]
        quotient_max = {1: 5, 2: 10, 3: 20, 4: 50, 5: 100}[difficulty]
        a = rng.randint(2, divisor_max)
        b = rng.randint(1, quotient_max)
        answer = b
        b, a = b * a, a
        symbol = "÷"
    elif operation == "signed_addition":
        bound = {1: 5, 2: 10, 3: 20, 4: 50, 5: 100}[difficulty]
        a, b = rng.randint(-bound, bound), rng.randint(-bound, bound)
        answer = a + b
        symbol = "+"
    elif operation == "signed_multiplication":
        bound = {1: 5, 2: 10, 3: 12, 4: 20, 5: 30}[difficulty]
        a, b = rng.randint(-bound, bound), rng.randint(-bound, bound)
        answer = a * b
        symbol = "×"
    else:
        raise ValueError(f"Aucun générateur fiable pour la compétence : {skill.id}")

    return Question(skill.id, f"{a} {symbol} {b} = ?", answer, (a, b), operation)


def generate_question(skill_id: str, difficulty: int = 1, seed: int | None = None) -> Question:
    """Generate one question. Supplying a seed makes it reproducible."""
    skill = get_skill(skill_id)
    return _integer_question(skill, difficulty, random.Random(seed))


def generate_session(
    skill_id: str,
    count: int,
    difficulty: int = 1,
    seed: int | None = None,
    avoid_duplicates: bool = True,
) -> tuple[Question, ...]:
    """Generate a finite session with bounded retries and clear constraints."""
    if count < 1:
        raise ValueError("Une séance doit contenir au moins une question.")
    if count > 500:
        raise ValueError("Une séance ne peut pas dépasser 500 questions.")
    rng = random.Random(seed)
    skill = get_skill(skill_id)
    questions: list[Question] = []
    seen: set[tuple[str, int, int]] = set()
    max_attempts = max(100, count * 30)

    for _ in range(max_attempts):
        if len(questions) >= count:
            break
        question = _integer_question(skill, difficulty, rng)
        if avoid_duplicates and question.signature in seen:
            continue
        seen.add(question.signature)
        questions.append(question)

    if len(questions) != count:
        raise ValueError(
            f"Impossible de générer {count} questions distinctes pour {skill_id} "
            f"à la difficulté {difficulty}. Réduisez le nombre de questions ou augmentez la difficulté."
        )
    return tuple(questions)


def check_answer(question: Question, response: str | int) -> bool:
    """Compare an answer without accepting malformed or non-integer input."""
    try:
        value = int(str(response).strip())
    except (TypeError, ValueError):
        return False
    return value == question.answer
