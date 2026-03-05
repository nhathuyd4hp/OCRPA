FROM python:3.12.9

ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

EXPOSE 5678

CMD ["python","-m","uvicorn","src.main:app","--host","0.0.0.0","--port","5678"]
