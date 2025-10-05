# celery-beat/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY Celery-Beat/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the required backend files and folders
COPY ../BackEnd/models.py ./
COPY ../BackEnd/database.py ./
COPY ../BackEnd/schemas.py ./
COPY ../BackEnd/services/jsearch_service.py ./services/jsearch_service.py
COPY ../BackEnd/utils/resume_parser.py ./utils/resume_parser.py
RUN mkdir -p services utils && touch services/__init__.py utils/__init__.py

# Copy celery beat code
COPY ../Celery-Worker/celery_app.py ./
COPY ../Celery-Worker/tasks/ ./tasks/

# Set PYTHONPATH so Python can find modules
ENV PYTHONPATH=/app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser

CMD ["celery", "-A", "celery_app", "beat", "--loglevel=info"]