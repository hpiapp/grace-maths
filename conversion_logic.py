"""Multiple-choice questions for fractions, decimals, and percentages."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ChoiceQuestion:
    kind: str
    prompt: str
    options: tuple[str, ...]
    answer: str
    hint: str
    explanation: str

    @property
    def display_answer(self) -> str:
        return self.answer


@dataclass(frozen=True)
class ConversionFact:
    fraction: str
    decimal: str
    percentage: str


CONVERSION_FACTS = (
    ConversionFact("1/2", "0.5", "50%"),
    ConversionFact("1/4", "0.25", "25%"),
    ConversionFact("3/4", "0.75", "75%"),
    ConversionFact("1/5", "0.2", "20%"),
    ConversionFact("2/5", "0.4", "40%"),
    ConversionFact("3/5", "0.6", "60%"),
    ConversionFact("4/5", "0.8", "80%"),
    ConversionFact("1/10", "0.1", "10%"),
    ConversionFact("3/10", "0.3", "30%"),
    ConversionFact("7/10", "0.7", "70%"),
    ConversionFact("1/20", "0.05", "5%"),
    ConversionFact("3/20", "0.15", "15%"),
    ConversionFact("1/8", "0.125", "12.5%"),
    ConversionFact("3/8", "0.375", "37.5%"),
    ConversionFact("5/8", "0.625", "62.5%"),
    ConversionFact("7/8", "0.875", "87.5%"),
)


@dataclass(frozen=True)
class PriceScenario:
    item: str
    original: int
    reduction: int
    sale: int
    restore_percentage: str


PRICE_SCENARIOS = (
    PriceScenario("headphones", 80, 25, 60, "33⅓%"),
    PriceScenario("trainers", 60, 25, 45, "33⅓%"),
    PriceScenario("coat", 120, 25, 90, "33⅓%"),
    PriceScenario("book set", 40, 25, 30, "33⅓%"),
    PriceScenario("board game", 50, 20, 40, "25%"),
    PriceScenario("bicycle", 200, 20, 160, "25%"),
    PriceScenario("lamp", 40, 50, 20, "100%"),
)


def _options(answer: str, pool: tuple[str, ...], rng: random.Random) -> tuple[str, ...]:
    alternatives = list(dict.fromkeys(option for option in pool if option != answer))
    chosen = [answer, *rng.sample(alternatives, 3)]
    rng.shuffle(chosen)
    return tuple(chosen)


def _money(value: float) -> str:
    return f"£{int(value)}" if value.is_integer() else f"£{value:.2f}"


def build_conversion_bank(rng: random.Random | None = None) -> list[ChoiceQuestion]:
    """Build fraction/decimal/percentage conversion questions."""
    rng = rng or random.Random()
    fractions = tuple(fact.fraction for fact in CONVERSION_FACTS)
    decimals = tuple(fact.decimal for fact in CONVERSION_FACTS)
    percentages = tuple(fact.percentage for fact in CONVERSION_FACTS)
    questions: list[ChoiceQuestion] = []

    templates = (
        ("fraction_to_percentage", "What is {fraction} as a percentage?", "percentage", percentages),
        ("percentage_to_fraction", "What is {percentage} as a fraction in its simplest form?", "fraction", fractions),
        ("decimal_to_percentage", "What is {decimal} as a percentage?", "percentage", percentages),
        ("percentage_to_decimal", "What is {percentage} as a decimal?", "decimal", decimals),
        ("fraction_to_decimal", "What is {fraction} as a decimal?", "decimal", decimals),
        ("decimal_to_fraction", "What is {decimal} as a fraction in its simplest form?", "fraction", fractions),
    )

    for fact in CONVERSION_FACTS:
        explanation = f"{fact.fraction} = {fact.decimal} = {fact.percentage}"
        values = {
            "fraction": fact.fraction,
            "decimal": fact.decimal,
            "percentage": fact.percentage,
        }
        for kind, prompt, target, pool in templates:
            answer = values[target]
            questions.append(
                ChoiceQuestion(
                    kind=kind,
                    prompt=prompt.format(**values),
                    options=_options(answer, pool, rng),
                    answer=answer,
                    hint="Choose the equivalent value.",
                    explanation=explanation,
                )
            )
    return questions


def build_percentage_change_pairs(
    rng: random.Random | None = None,
) -> list[tuple[ChoiceQuestion, ChoiceQuestion, ChoiceQuestion]]:
    """Build paired price-change questions, including the journey back to the original."""
    rng = rng or random.Random()
    restore_pool = ("20%", "25%", "33⅓%", "40%", "50%", "75%", "100%")
    pairs: list[tuple[ChoiceQuestion, ChoiceQuestion, ChoiceQuestion]] = []

    for scenario in PRICE_SCENARIOS:
        original = float(scenario.original)
        sale = float(scenario.sale)
        discount = original - sale
        repeated_increase = sale * (1 + scenario.reduction / 100)
        money_pool = tuple(
            dict.fromkeys(
                _money(value)
                for value in (
                    sale,
                    original,
                    original + discount,
                    original - discount / 2,
                    repeated_increase,
                    sale - discount,
                )
                if value >= 0
            )
        )

        decrease = ChoiceQuestion(
            kind="percentage_decrease",
            prompt=(
                f"Some {scenario.item} cost £{scenario.original}. "
                f"The price is reduced by {scenario.reduction}%. What is the sale price?"
            ),
            options=_options(_money(sale), money_pool, rng),
            answer=_money(sale),
            hint="Find the reduction, then subtract it from the original price.",
            explanation=(
                f"{scenario.reduction}% of £{scenario.original} is {_money(discount)}, "
                f"so £{scenario.original} − {_money(discount)} = {_money(sale)}."
            ),
        )

        restore = ChoiceQuestion(
            kind="percentage_restore",
            prompt=(
                f"The {scenario.item} fell from £{scenario.original} to £{scenario.sale}. "
                f"By what percentage must the current £{scenario.sale} price increase to return to £{scenario.original}?"
            ),
            options=_options(scenario.restore_percentage, restore_pool, rng),
            answer=scenario.restore_percentage,
            hint="Compare the amount added with the current price—not the old price.",
            explanation=(
                f"It must rise by {_money(discount)}. Compared with the current £{scenario.sale}, "
                f"that is {scenario.restore_percentage}. The percentage uses a new starting value."
            ),
        )

        same_increase = ChoiceQuestion(
            kind="percentage_same_increase",
            prompt=(
                f"The £{scenario.original} {scenario.item} is reduced by {scenario.reduction}% to £{scenario.sale}. "
                f"It then rises by the same {scenario.reduction}%. What is its final price?"
            ),
            options=_options(_money(repeated_increase), money_pool, rng),
            answer=_money(repeated_increase),
            hint="The increase is calculated from the lower, current price.",
            explanation=(
                f"{scenario.reduction}% of the current £{scenario.sale} is "
                f"{_money(repeated_increase - sale)}, so the final price is {_money(repeated_increase)}—"
                f"not the original £{scenario.original}."
            ),
        )
        pairs.append((decrease, restore, same_increase))

    return pairs


def make_conversion_quiz(
    mode: str,
    question_count: int,
    rng: random.Random | None = None,
) -> list[ChoiceQuestion]:
    """Make a balanced quiz and guarantee both directions of percentage change."""
    rng = rng or random.Random()
    conversion_bank = build_conversion_bank(rng)
    change_pairs = build_percentage_change_pairs(rng)

    if mode == "Conversions":
        bank = conversion_bank
        required: list[ChoiceQuestion] = []
    elif mode in {"Mixed practice", "Percentage change"}:
        chosen_pair = rng.choice(change_pairs)
        # Always include decrease-from-original and increase-from-current.
        required = [chosen_pair[0], chosen_pair[1]]
        change_bank = [question for pair in change_pairs for question in pair if question not in required]
        if mode == "Percentage change":
            bank = change_bank
        else:
            remaining = max(0, question_count - len(required))
            conversion_count = max(1, (remaining + 1) // 2)
            rng.shuffle(conversion_bank)
            rng.shuffle(change_bank)
            bank = [*conversion_bank[:conversion_count], *change_bank[: remaining - conversion_count]]
    else:
        raise ValueError(f"Unknown conversion quiz mode: {mode}")

    rng.shuffle(required)
    rng.shuffle(bank)
    quiz = required + bank[: max(0, question_count - len(required))]
    rng.shuffle(quiz)
    return quiz[:question_count]


def check_choice(question: ChoiceQuestion, selected_answer: str) -> bool:
    return selected_answer == question.answer
