"""Question generation and answer checking for Prime & Cube practice."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Iterable


PRIMES_TO_100 = (
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
)


@dataclass(frozen=True)
class Question:
    kind: str
    prompt: str
    answer: tuple[int, ...]
    hint: str

    @property
    def display_answer(self) -> str:
        if self.kind == "prime":
            return ", ".join(str(number) for number in self.answer)
        return str(self.answer[0])


def primes_between(lower: int, upper: int) -> tuple[int, ...]:
    """Return all primes in the inclusive range."""
    return tuple(number for number in PRIMES_TO_100 if lower <= number <= upper)


def build_question_bank(mode: str) -> list[Question]:
    """Build the question bank for the selected quiz mode."""
    questions: list[Question] = []

    if mode in {"Mixed", "Prime numbers"}:
        ranges = [(1, 10)] + [(start, start + 10) for start in range(10, 100, 10)]
        questions.extend(
            Question(
                kind="prime",
                prompt=f"What are the prime numbers between {lower} and {upper}?",
                answer=primes_between(lower, upper),
                hint="Enter every prime, separated by spaces or commas.",
            )
            for lower, upper in ranges
        )

    if mode in {"Mixed", "Cube numbers"}:
        questions.extend(
            Question(
                kind="cube",
                prompt=f"What is {number}³?",
                answer=(number**3,),
                hint="Enter one number.",
            )
            for number in range(1, 13)
        )

    return questions


def make_quiz(mode: str, question_count: int, rng: random.Random | None = None) -> list[Question]:
    """Create a shuffled quiz, cycling the bank only when necessary."""
    rng = rng or random.Random()
    bank = build_question_bank(mode)
    if not bank:
        raise ValueError(f"Unknown quiz mode: {mode}")

    quiz: list[Question] = []
    while len(quiz) < question_count:
        batch = bank.copy()
        rng.shuffle(batch)
        if quiz and len(batch) > 1 and batch[0] == quiz[-1]:
            batch[0], batch[1] = batch[1], batch[0]
        quiz.extend(batch)
    return quiz[:question_count]


def parse_numbers(raw_answer: str) -> tuple[int, ...] | None:
    """Parse positive whole numbers separated by common punctuation/words."""
    cleaned = raw_answer.strip().lower()
    if not cleaned:
        return None

    # Remove acceptable separators, then reject any remaining non-numeric text.
    remainder = re.sub(r"\band\b|[,;&+/\s-]+|\d+", "", cleaned)
    if remainder:
        return None

    numbers = re.findall(r"\d+", cleaned)
    if not numbers:
        return None
    return tuple(sorted({int(number) for number in numbers}))


def check_answer(question: Question, raw_answer: str) -> bool:
    parsed = parse_numbers(raw_answer)
    if parsed is None:
        return False
    return parsed == tuple(sorted(question.answer))


def average(values: Iterable[float]) -> float:
    values = tuple(values)
    return sum(values) / len(values) if values else 0.0
