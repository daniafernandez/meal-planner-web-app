import re
from fractions import Fraction
from typing import ClassVar

from pydantic import BaseModel

from models.generic_unit import GenericUnit, MEASUREMENT_TYPE_NAMES
from models.ingredient.ingredient import Ingredient
from models.ingredient.ingredient_unit import IngredientUnit
from models.ingredient.size_description import QualitativeDescription, QuantitativeDescription
from models.recipe.recipe_ingredient_quantity import RecipeIngredientQuantity


class ParsedRecipeIngredient(BaseModel):
    quantity: RecipeIngredientQuantity
    ingredient: Ingredient | None = None
    unit: IngredientUnit | None = None


class RecipeIngredientParser:
    NUMBER_WORDS: ClassVar[dict[str, float]] = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
    }
    SCALE_WORDS: ClassVar[dict[str, float]] = {
        "hundred": 100,
        "thousand": 1000,
    }
    FRACTION_WORDS: ClassVar[dict[str, float]] = {
        "half": 0.5,
        "halves": 0.5,
        "quarter": 0.25,
        "quarters": 0.25,
        "third": 1 / 3,
        "thirds": 1 / 3,
        "fourth": 0.25,
        "fourths": 0.25,
    }
    ARTICLE_WORDS: ClassVar[dict[str, float]] = {
        "a": 1,
        "an": 1,
    }
    MULTIPLIER_WORDS: ClassVar[dict[str, float]] = {
        "dozen": 12,
    }
    UNICODE_FRACTIONS: ClassVar[dict[str, str]] = {
        "¼": "1/4",
        "½": "1/2",
        "¾": "3/4",
        "⅓": "1/3",
        "⅔": "2/3",
        "⅛": "1/8",
        "⅜": "3/8",
        "⅝": "5/8",
        "⅞": "7/8",
    }

    def parse(self, ingredient_line_string: str) -> ParsedRecipeIngredient:
        return ParsedRecipeIngredient(
            quantity=self.parse_quantity(ingredient_line_string),
            ingredient=self.parse_ingredient(ingredient_line_string),
            unit=self.parse_unit(ingredient_line_string),
        )

    def parse_quantity(self, ingredient_line_string: str) -> RecipeIngredientQuantity:
        tokens = self._tokenize_ingredient_line(ingredient_line_string)
        alpha_quantity = self._get_leading_alpha_quantity(tokens)
        if alpha_quantity is not None:
            return RecipeIngredientQuantity(
                numeric_quantity=RecipeIngredientQuantity.ALPHA_QUANTITY_ESTIMATES.get(
                    alpha_quantity,
                    1,
                ),
                alpha_quantity=alpha_quantity,
            )

        quantity_tokens = self._get_leading_numeric_quantity_tokens(tokens)
        if not quantity_tokens:
            return RecipeIngredientQuantity(numeric_quantity=1)

        return RecipeIngredientQuantity(
            numeric_quantity=self._convert_quantity_tokens_to_number(quantity_tokens),
        )

    def parse_ingredient(self, ingredient_line_string: str) -> Ingredient | None:
        return None

    def parse_unit(self, ingredient_line_string: str) -> IngredientUnit | None:
        tokens = self._tokens_after_leading_quantity(
            self._tokenize_ingredient_line(ingredient_line_string),
        )
        if not tokens:
            return None

        size = None
        if tokens[0] in {"small", "medium", "large"}:
            size = QualitativeDescription(quality=tokens[0])
            tokens = tokens[1:]
        elif (
            len(tokens) >= 2
            and self._is_numeric_token(tokens[0])
            and self._get_leading_explicit_unit_name(tokens[1:]) is not None
        ):
            size = QuantitativeDescription(
                quantity=int(self._numeric_token_to_float(tokens[0])),
                generic_unit=GenericUnit(
                    name=self._get_leading_explicit_unit_name(tokens[1:]),
                ),
            )
            tokens = tokens[2:]

        return IngredientUnit(
            generic_unit=GenericUnit(name=self._infer_generic_unit_name(tokens)),
            size=size,
            gram_weight=100,
        )

    @classmethod
    def _tokenize_ingredient_line(cls, ingredient_line_string: str) -> list[str]:
        normalized = ingredient_line_string.lower()
        for unicode_fraction, ascii_fraction in cls.UNICODE_FRACTIONS.items():
            normalized = normalized.replace(unicode_fraction, f" {ascii_fraction} ")
        normalized = normalized.replace("-", " ")
        return re.findall(r"\d+\s*/\s*\d+|\d+(?:\.\d+)?|[a-z]+", normalized)

    @classmethod
    def _get_leading_alpha_quantity(cls, tokens: list[str]) -> str | None:
        alpha_phrases = sorted(
            RecipeIngredientQuantity.ALPHA_QUANTITY_ESTIMATES,
            key=lambda phrase: len(phrase.split()),
            reverse=True,
        )
        for phrase in alpha_phrases:
            phrase_tokens = phrase.split()
            if tokens[: len(phrase_tokens)] == phrase_tokens:
                return phrase
        return None

    @classmethod
    def _tokens_after_leading_quantity(cls, tokens: list[str]) -> list[str]:
        alpha_quantity = cls._get_leading_alpha_quantity(tokens)
        if alpha_quantity is not None:
            return tokens[len(alpha_quantity.split()) :]

        numeric_quantity_tokens = cls._get_leading_numeric_quantity_tokens(tokens)
        return tokens[len(numeric_quantity_tokens) :]

    @classmethod
    def _infer_generic_unit_name(cls, tokens: list[str]) -> str:
        explicit_unit_name = cls._get_leading_explicit_unit_name(tokens)
        if explicit_unit_name is not None:
            return explicit_unit_name
        return "count"

    @classmethod
    def _get_leading_explicit_unit_name(cls, tokens: list[str]) -> str | None:
        unit_names = {
            unit_name
            for measurement_type_names in MEASUREMENT_TYPE_NAMES.values()
            for unit_name in measurement_type_names
        }
        for token_count in range(min(3, len(tokens)), 0, -1):
            unit_name = " ".join(tokens[:token_count])
            if unit_name in unit_names:
                return unit_name
        return None

    @classmethod
    def _get_leading_numeric_quantity_tokens(cls, tokens: list[str]) -> list[str]:
        quantity_tokens: list[str] = []
        for index, token in enumerate(tokens):
            if token == "and" and quantity_tokens:
                quantity_tokens.append(token)
                continue
            if cls._starts_quantitative_size(tokens, index, quantity_tokens):
                break
            if cls._is_quantity_token(token):
                quantity_tokens.append(token)
                continue
            break
        return quantity_tokens

    @classmethod
    def _starts_quantitative_size(
        cls,
        tokens: list[str],
        index: int,
        quantity_tokens: list[str],
    ) -> bool:
        if not quantity_tokens or index + 1 >= len(tokens):
            return False
        token = tokens[index]
        return (
            cls._is_numeric_token(token)
            and "/" not in token
            and cls._get_leading_explicit_unit_name(tokens[index + 1 :]) is not None
        )

    @classmethod
    def _is_quantity_token(cls, token: str) -> bool:
        return (
            cls._is_numeric_token(token)
            or token in cls.NUMBER_WORDS
            or token in cls.SCALE_WORDS
            or token in cls.FRACTION_WORDS
            or token in cls.ARTICLE_WORDS
            or token in cls.MULTIPLIER_WORDS
        )

    @classmethod
    def _convert_quantity_tokens_to_number(cls, tokens: list[str]) -> float:
        total = 0.0
        current = 0.0
        index = 0

        while index < len(tokens):
            token = tokens[index]
            next_token = tokens[index + 1] if index + 1 < len(tokens) else None

            if token == "and":
                index += 1
                continue

            if next_token in cls.FRACTION_WORDS and cls._can_modify_fraction(token):
                current += cls._fraction_numerator(token) * cls.FRACTION_WORDS[next_token]
                index += 2
                continue

            if cls._is_numeric_token(token):
                current += cls._numeric_token_to_float(token)
            elif token in cls.NUMBER_WORDS:
                current += cls.NUMBER_WORDS[token]
            elif token in cls.ARTICLE_WORDS:
                current += cls.ARTICLE_WORDS[token]
            elif token in cls.FRACTION_WORDS:
                current += cls.FRACTION_WORDS[token]
            elif token in cls.MULTIPLIER_WORDS:
                current = (current or 1) * cls.MULTIPLIER_WORDS[token]
            elif token in cls.SCALE_WORDS:
                current = (current or 1) * cls.SCALE_WORDS[token]
                if cls.SCALE_WORDS[token] >= 1000:
                    total += current
                    current = 0.0

            index += 1

        return total + current

    @classmethod
    def _can_modify_fraction(cls, token: str) -> bool:
        return (
            cls._is_numeric_token(token)
            or token in cls.NUMBER_WORDS
            or token in cls.ARTICLE_WORDS
        )

    @classmethod
    def _fraction_numerator(cls, token: str) -> float:
        if token in cls.ARTICLE_WORDS:
            return cls.ARTICLE_WORDS[token]
        if cls._is_numeric_token(token):
            return cls._numeric_token_to_float(token)
        return cls.NUMBER_WORDS[token]

    @staticmethod
    def _is_numeric_token(token: str) -> bool:
        return bool(re.fullmatch(r"\d+\s*/\s*\d+|\d+(?:\.\d+)?", token))

    @staticmethod
    def _numeric_token_to_float(token: str) -> float:
        if "/" in token:
            return float(Fraction(token.replace(" ", "")))
        return float(token)
