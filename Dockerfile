FROM python:3.10-slim

WORKDIR /opt/api-fiap
EXPOSE 8000

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./configuration/* ./configuration/
COPY ./.env ./
COPY ./logging.conf ./
COPY ./main.py ./
COPY ./tests/* ./tests/

ENTRYPOINT ["fastapi", "run", "main.py"]
