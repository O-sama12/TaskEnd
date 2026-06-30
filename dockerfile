FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# system dependencies (for postgres + build tools)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app/

# collect static files (optional for later)
# RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]