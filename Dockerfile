FROM python:3.12.3-alpine

ARG JWT_SECRET_KEY
ARG DATABASE_URL

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV JWT_SECRET_KEY=$JWT_SECRET_KEY
ENV DATABASE_URL=$DATABASE_URL

WORKDIR /balbalm

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
