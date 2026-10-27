# Verification image: builds the task state and runs its pytest suite.
FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir "pytest>=8,<9"

COPY src/ src/
COPY tests/ tests/

CMD ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]
