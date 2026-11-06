import uvicorn

from fastapi import FastAPI, Body

from app.schemas.schemas import Person

app = FastAPI(docs_url='/swagger')

SINGLE_SURNAME={'summary': 'Одна фамилия',
                    'description': 'Одиночная фамилия передается строкой',
                    'value': {
                       'name': 'Taras',
                       'surname': 'Belov',
                       'age': 20,
                       'is_staff': False,
                       'education_level': 'Среднее образование'}}
MULTIPLE_SURNAME={
                    'summary': 'Несколько фамилий',
                    'description': 'Несколько фамилий передаются списком',
                    'value': {
                       'name': 'Eduardo',
                       'surname': ['Santos', 'Tavares'],
                       'age': 20,
                       'is_staff': False,
                       'education_level': 'Высшее образование'
                    }
                }
INVALID={
                    'summary': 'Некорректный запрос',
                    'description': 'Возраст передается только целым числом',
                    'value': {
                        'name': 'Eduardo',
                        'surname': ['Santos', 'Tavares'],
                        'age': 'forever young',
                        'is_staff': False,
                        'education_level': 'Среднее специальное образование'
                    }
                }


@app.post('/hello')
def greetings(person: Person = Body(
            ...,
            openapi_examples={
                # Первый пример.
                'single_surname': SINGLE_SURNAME,
                # Второй пример.
                'multiple_surnames': MULTIPLE_SURNAME,
                # Третий пример.
                'invalid': INVALID
            }
        )
) -> dict[str, str]:
    """
    Приветствие пользователя:

    - **name**: имя
    - **surname**: фамилия или несколько фамилий
    - **age**: возраст (опционально)
    - **title**: обращение
    """
    if isinstance(person.surname, list):
        surnames = ' '.join(person.surname)
    else:
        surnames = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)