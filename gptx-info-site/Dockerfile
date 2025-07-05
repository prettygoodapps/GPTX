FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry

# Copy poetry project files and install dependencies
COPY pyproject.toml ./
RUN poetry install --no-root

# Copy the rest of your application code
COPY . .
RUN sed -i 's/@MappedAsDataclass/MappedAsDataclass/g' /app/src/gptx/core/database.py
RUN cat /app/src/gptx/core/database.py

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "gptx.main:app", "--host", "0.0.0.0", "--port", "8000"]
