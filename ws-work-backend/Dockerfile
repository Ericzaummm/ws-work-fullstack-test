FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Executa o seed.py PRIMEIRO (&&) e só depois sobe o servidor Uvicorn.
# Como o seed.py tem o comando drop_all(), isso garante que toda vez que alguém 
# subir o projeto, ele terá um banco limpo, populado e sem erros!
CMD ["sh", "-c", "python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]