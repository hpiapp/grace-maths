# Grace Maths Practice

A Streamlit practice app for learning:

- prime numbers up to 100
- cube numbers from 1³ to 12³
- conversions between fractions, decimals, and percentages
- percentage decreases and the percentage increase needed to restore an original price

## Run locally

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Choose this repository in Streamlit Community Cloud and use:

- Branch: `main`
- Main file path: `app.py`
- Python version: `3.12`

The app includes randomised questions, mental-maths-friendly multiple choice, response timing, flexible prime-number input, streaks, scoring, explanations, and answer review.

Every mixed fractions-and-percentages session includes both sides of a price change. For example, reducing £80 by 25% gives £60, but returning from £60 to £80 requires a 33⅓% increase—not 25%.

The conversion practice has three difficulty levels:

- **Warm-up:** familiar equivalences and direct price changes
- **Stretch:** eighths, reverse percentages, and less obvious mental calculations
- **Challenge:** thirds and sixteenths, compound changes, deal comparisons, and changed starting values

## Run the tests

```bash
python3 -m unittest -v
```
