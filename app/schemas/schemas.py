import re
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, ConfigDict,field_validator,model_validator


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str = Field(..., min_length=2, max_length=20,
                      title='Full name', description='You can write in any case upper or lower case')
    surname: Union[str, list[str]] = Field(..., min_length=2, max_length=50)
    age: Optional[int] = Field(
        None,
        ge=4,
        le=99,
        description='Возраст от 5 до 99 лет включительно',
    )
    is_staff: bool = Field(
        False,
        alias='is-staff',
        description='Флаг сотрудника компании',
    )
    education_level: Optional[EducationLevel] = Field(
        None,
        description='Уровень образования',
    )

    model_config = ConfigDict(
        title='Class for greetings',
        extra='forbid',
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'name': 'Eduardo',
                'surname': ['Santos', 'Tavares'],
                'age': 20,
                'is_staff': False,
                'education_level': 'Среднее образование'
            }
        }
    )

    @field_validator('name')
    @classmethod
    def name_cant_numeric(cls, value: str) -> str:
        if value.isnumeric():
            raise ValueError('Name can not be numeric')
        return value

    @model_validator(mode="after")
    def using_different_languages(self):
        if isinstance(self.surname, list):
            surname = ''.join(self.surname)
        else:
            surname = self.surname

        checked_value = f"{self.name} {surname}"

        has_cyr = re.search('[а-яё]', checked_value,re.IGNORECASE)
        has_lat = re.search('[a-z]', checked_value,re.IGNORECASE)

        if has_cyr and has_lat:
            raise ValueError('Please, do not shake russian and latin letters')

        return self
