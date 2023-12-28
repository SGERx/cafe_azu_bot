from typing import Any
from app.models.dinner_sets import DinnerSet
from app.schemas.dinnerset_schema import DinnerSetDB


def map_orm_to_pydantic(sets: list[DinnerSet]) -> list[DinnerSetDB]:
    pydantic_objs: list[DinnerSetDB] = [
        DinnerSetDB.model_validate(dish) for dish in sets
    ]

    return pydantic_objs


def map_orm_to_pydantic2(sets: list[Any], schema) -> list[Any]:
    pydantic_objs: list[schema] = [schema.model_validate(dish) for dish in sets]

    return pydantic_objs


def map_pydantic_to_json(sets: list[DinnerSetDB]) -> list[dict[str, str]]:
    json_objs: list[dict[str, str]] = [dish.model_dump_json() for dish in sets]

    return json_objs


def map_json_to_pydantic(sets: list[dict[str, str]]) -> list[DinnerSetDB]:
    pydantic_objs: list[DinnerSetDB] = [
        DinnerSetDB.model_validate_json(dish) for dish in sets
    ]

    return pydantic_objs
