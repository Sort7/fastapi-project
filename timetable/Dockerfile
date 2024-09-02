FROM python:3.11

#ENV C_FORCE_ROOT=True
#ENV PYTHONUNBUFFERED=1
#ENV PYTHONPATH=/code
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1


WORKDIR /code
# WORKDIR /usr/src/app

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.8.3

RUN apt-get clean && apt-get update

COPY ../poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

#COPY pyproject.toml poetry.lock /code/

#RUN poetry config virtualenvs.create fatimetablelse \
#    && poetry install --no-interaction --no-ansi --without dev \
#    && echo yes | poetry cache clear . --all \


COPY .. /code

CMD ["uvicorn", "timetable.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
