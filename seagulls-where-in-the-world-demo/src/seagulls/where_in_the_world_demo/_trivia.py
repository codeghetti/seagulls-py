import os

import openai
import random
import re

COUNTRIES = [
    "argentina",
    "australia",
    "colombia",
    "ethiopia",
    "germany",
    "guatemala",
    "india",
    "indonesia",
    "italy",
    "romania",
    "united kingdom",
    "united states",
    "japan",
    "senegal",
    "south africa"
]

FOOD_PROMPT = """
Generate a list of 15 food names from {country}, one per line.

1."""

TRIVIA_PROMPT = """
Generate a detailed trivia question for the dish {food} from {country}. The question should be in the form of "What is country makes ...?".
Include details about taste, color, texture, common spices, and preparation method.
The question should not reveal the name of the country, or the name of the dish.

Q:"""


def get_completion(prompt) -> str:
    openai.api_key = os.environ["OPENAI_KEY"]

    result = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=256,
        stop=["\nA:", "\n\n"],
    )

    text = result["choices"][0]["text"]

    return text


def get_foods(country):
    prompt = FOOD_PROMPT.format(country=country)
    output = get_completion(prompt)
    # use a regex to remove the leading numbers
    foods = [re.sub(r"\d+\.", "", f).strip() for f in output.strip().split("\n")]
    return foods


def get_food_trivia(food, country):
    prompt = TRIVIA_PROMPT.format(food=food, country=country)
    output = get_completion(prompt)
    return output.strip()


if __name__ == "__main__":
    country = random.choice(COUNTRIES)
    print(f"Country: {country}")
    food = random.choice(get_foods(country))
    print(f"Food: {food}")
    trivia = get_food_trivia(food, country)
    print(trivia)
