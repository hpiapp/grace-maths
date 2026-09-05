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
    difficulty: str


CONVERSION_FACTS = (
    ConversionFact("1/2", "0.5", "50%", "Warm-up"),
    ConversionFact("1/4", "0.25", "25%", "Warm-up"),
    ConversionFact("3/4", "0.75", "75%", "Warm-up"),
    ConversionFact("1/5", "0.2", "20%", "Warm-up"),
    ConversionFact("2/5", "0.4", "40%", "Warm-up"),
    ConversionFact("3/5", "0.6", "60%", "Warm-up"),
    ConversionFact("4/5", "0.8", "80%", "Warm-up"),
    ConversionFact("1/10", "0.1", "10%", "Warm-up"),
    ConversionFact("3/10", "0.3", "30%", "Warm-up"),
    ConversionFact("7/10", "0.7", "70%", "Warm-up"),
    ConversionFact("1/20", "0.05", "5%", "Warm-up"),
    ConversionFact("3/20", "0.15", "15%", "Warm-up"),
    ConversionFact("1/8", "0.125", "12.5%", "Stretch"),
    ConversionFact("3/8", "0.375", "37.5%", "Stretch"),
    ConversionFact("5/8", "0.625", "62.5%", "Stretch"),
    ConversionFact("7/8", "0.875", "87.5%", "Stretch"),
    ConversionFact("11/20", "0.55", "55%", "Stretch"),
    ConversionFact("13/20", "0.65", "65%", "Stretch"),
    ConversionFact("17/20", "0.85", "85%", "Stretch"),
    ConversionFact("19/20", "0.95", "95%", "Stretch"),
    ConversionFact("1/3", "0.333…", "33⅓%", "Challenge"),
    ConversionFact("2/3", "0.666…", "66⅔%", "Challenge"),
    ConversionFact("1/6", "0.166…", "16⅔%", "Challenge"),
    ConversionFact("5/6", "0.833…", "83⅓%", "Challenge"),
    ConversionFact("1/16", "0.0625", "6.25%", "Challenge"),
    ConversionFact("3/16", "0.1875", "18.75%", "Challenge"),
    ConversionFact("5/16", "0.3125", "31.25%", "Challenge"),
    ConversionFact("7/16", "0.4375", "43.75%", "Challenge"),
)


@dataclass(frozen=True)
class PriceScenario:
    item: str
    original: int
    reduction: int
    sale: int
    restore_percentage: str


PRICE_SCENARIOS = {
    "Warm-up": (
        PriceScenario("headphones", 80, 25, 60, "33⅓%"),
        PriceScenario("trainers", 60, 25, 45, "33⅓%"),
        PriceScenario("coat", 120, 25, 90, "33⅓%"),
        PriceScenario("book set", 40, 25, 30, "33⅓%"),
        PriceScenario("board game", 50, 20, 40, "25%"),
        PriceScenario("bicycle", 200, 20, 160, "25%"),
        PriceScenario("lamp", 40, 50, 20, "100%"),
    ),
    "Stretch": (
        PriceScenario("jacket", 72, 25, 54, "33⅓%"),
        PriceScenario("concert ticket", 90, 20, 72, "25%"),
        PriceScenario("desk", 80, 40, 48, "66⅔%"),
        PriceScenario("sports kit", 84, 50, 42, "100%"),
    ),
    "Challenge": (
        PriceScenario("tablet", 280, 25, 210, "33⅓%"),
        PriceScenario("weekend trip", 360, 20, 288, "25%"),
        PriceScenario("camera", 240, 40, 144, "66⅔%"),
        PriceScenario("season ticket", 336, 50, 168, "100%"),
    ),
}


def _options(answer: str, pool: tuple[str, ...], rng: random.Random) -> tuple[str, ...]:
    alternatives = list(dict.fromkeys(option for option in pool if option != answer))
    chosen = [answer, *rng.sample(alternatives, 3)]
    rng.shuffle(chosen)
    return tuple(chosen)


def _money(value: float) -> str:
    return f"£{int(value)}" if value.is_integer() else f"£{value:.2f}"


def build_conversion_bank(
    rng: random.Random | None = None,
    difficulty: str = "Warm-up",
) -> list[ChoiceQuestion]:
    """Build fraction/decimal/percentage conversion questions."""
    rng = rng or random.Random()
    facts = tuple(fact for fact in CONVERSION_FACTS if fact.difficulty == difficulty)
    if not facts:
        raise ValueError(f"Unknown difficulty: {difficulty}")
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

    for fact in facts:
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
    difficulty: str = "Warm-up",
) -> list[tuple[ChoiceQuestion, ChoiceQuestion, ChoiceQuestion]]:
    """Build paired price-change questions, including the journey back to the original."""
    rng = rng or random.Random()
    restore_pool = ("20%", "25%", "33⅓%", "40%", "50%", "75%", "100%")
    pairs: list[tuple[ChoiceQuestion, ChoiceQuestion, ChoiceQuestion]] = []

    scenarios = PRICE_SCENARIOS.get(difficulty)
    if scenarios is None:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    for scenario in scenarios:
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


def build_advanced_change_bank(
    difficulty: str,
    rng: random.Random | None = None,
) -> list[ChoiceQuestion]:
    """Build reverse and multi-step percentage questions for harder levels."""
    rng = rng or random.Random()
    if difficulty == "Warm-up":
        return []

    stretch_specs = (
        (
            "reverse_percentage",
            "A hoodie costs £72 after a 20% reduction. What was its original price?",
            "£90",
            ("£80", "£86.40", "£90", "£92"),
            "After 20% off, £72 is 80% of the original. One tenth is £9, so 100% is £90.",
        ),
        (
            "reverse_percentage",
            "A bag costs £54 after a 25% reduction. What was its original price?",
            "£72",
            ("£67.50", "£72", "£74", "£81"),
            "£54 is 75% of the original. Divide by 3 to get 25% (£18), then multiply by 4: £72.",
        ),
        (
            "reverse_percentage",
            "A chair costs £48 after a 40% reduction. What was its original price?",
            "£80",
            ("£67.20", "£72", "£80", "£88"),
            "£48 is the 60% left. If 60% is £48, then 10% is £8 and 100% is £80.",
        ),
        (
            "percentage_of_amount",
            "A £60 game console increases in price by 15%. What is the new price?",
            "£69",
            ("£66", "£69", "£72", "£75"),
            "10% of £60 is £6 and 5% is £3. Add £9 to £60 to get £69.",
        ),
        (
            "percentage_of_amount",
            "A £80 bicycle is reduced by 15%. What is the new price?",
            "£68",
            ("£65", "£68", "£72", "£76"),
            "10% of £80 is £8 and 5% is £4. Subtract £12 from £80 to get £68.",
        ),
        (
            "percentage_of_amount",
            "A shop takes 12.5% off a £64 skateboard. How much is the discount?",
            "£8",
            ("£6.40", "£8", "£12", "£16"),
            "12.5% is one eighth. £64 ÷ 8 = £8.",
        ),
        (
            "percentage_of_amount",
            "A £70 annual pass increases in price by 30%. What is the new price?",
            "£91",
            ("£79", "£88", "£91", "£100"),
            "10% of £70 is £7, so 30% is £21. Add £21 to £70 to get £91.",
        ),
        (
            "reverse_percentage",
            "A game costs £70 after a 12.5% reduction. What was its original price?",
            "£80",
            ("£77.50", "£78.75", "£80", "£82.50"),
            "12.5% is one eighth, so £70 is seven eighths. One eighth is £10 and eight eighths is £80.",
        ),
    )

    challenge_specs = (
        (
            "compound_change",
            "A £120 coat is reduced by 25%, then the sale price rises by 25%. What is the final price?",
            "£112.50",
            ("£90", "£105", "£112.50", "£120"),
            "£120 falls to £90. Then 25% of £90 is £22.50, giving £112.50—not £120.",
        ),
        (
            "compound_change",
            "A £200 laptop is reduced by 20%, then reduced by another 10%. What is the final price?",
            "£144",
            ("£140", "£144", "£150", "£160"),
            "20% off gives £160. A further 10% off £160 is £16, leaving £144.",
        ),
        (
            "compound_change",
            "A £80 ticket rises by 25%, then falls by 20%. What is the final price?",
            "£80",
            ("£76", "£80", "£84", "£100"),
            "£80 rises to £100. A 20% fall from £100 is £20, taking it back to £80.",
        ),
        (
            "percentage_difference",
            "A £120 coat falls by 25%, then rises by 25%. How far below the original price does it finish?",
            "£7.50",
            ("£0", "£6", "£7.50", "£15"),
            "It falls to £90, then rises to £112.50. That is £7.50 below £120.",
        ),
        (
            "compare_discounts",
            "Shop A takes 25% off £80. Shop B takes 20% off £75. Which sale price is lower?",
            "They are the same",
            ("Shop A", "Shop B", "They are the same", "Not enough information"),
            "Shop A charges £60. Shop B also charges £60, so the sale prices are equal.",
        ),
        (
            "compare_discounts",
            "Shop A takes 25% off £120. Shop B takes 15% off £100. Which is cheaper?",
            "Shop B by £5",
            ("Shop A by £5", "Shop B by £5", "Shop B by £10", "They are the same"),
            "Shop A charges £90. Shop B charges £85, which is £5 cheaper.",
        ),
        (
            "reverse_percentage",
            "A price is reduced by 15% and becomes £68. What was the original price?",
            "£80",
            ("£76", "£78.20", "£80", "£83"),
            "£68 is 85% of the original. Since 5% is £4, 100% is £80.",
        ),
        (
            "percentage_direction",
            "A price rises from £64 to £80, then falls from £80 to £64. Which statement is correct?",
            "Up 25%, then down 20%",
            ("Up 20%, then down 20%", "Up 25%, then down 20%", "Up 25%, then down 25%", "Up 16%, then down 16%"),
            "The £16 rise is 25% of £64. The £16 fall is 20% of £80 because the starting value changed.",
        ),
    )

    specs = stretch_specs if difficulty == "Stretch" else challenge_specs if difficulty == "Challenge" else None
    if specs is None:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    return [
        ChoiceQuestion(
            kind=kind,
            prompt=prompt,
            options=_options(answer, options, rng),
            answer=answer,
            hint="Work from the current starting value at each step.",
            explanation=explanation,
        )
        for kind, prompt, answer, options, explanation in specs
    ]


def make_conversion_quiz(
    mode: str,
    question_count: int,
    rng: random.Random | None = None,
    difficulty: str = "Warm-up",
) -> list[ChoiceQuestion]:
    """Make a balanced quiz and guarantee both directions of percentage change."""
    rng = rng or random.Random()
    conversion_bank = build_conversion_bank(rng, difficulty)
    change_pairs = build_percentage_change_pairs(rng, difficulty)
    advanced_bank = build_advanced_change_bank(difficulty, rng)

    if mode == "Conversions":
        bank = conversion_bank
        required: list[ChoiceQuestion] = []
    elif mode in {"Mixed practice", "Percentage change"}:
        chosen_pair = rng.choice(change_pairs)
        # Always include decrease-from-original and increase-from-current.
        required = [chosen_pair[0], chosen_pair[1]]
        change_bank = [question for pair in change_pairs for question in pair if question not in required]
        if advanced_bank and question_count >= 3:
            advanced_question = rng.choice(advanced_bank)
            required.append(advanced_question)
            advanced_bank.remove(advanced_question)
        change_bank.extend(advanced_bank)
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
