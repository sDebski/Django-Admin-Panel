FROM python:3.10-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*


RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt,readonly \
    python -m pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --no-input

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.8000"]