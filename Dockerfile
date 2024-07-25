FROM python:3.12-slim

# Argumento que carrega o nome da imagem com valor padrão e pode ser sobrescrito no momento do build
ARG IMAGE_NAME=embrapa-data-api

WORKDIR /opt/${IMAGE_NAME}
EXPOSE 8000

# Atualiza a imagem e instala algumas libs e o Google Chrome
RUN apt update
RUN apt install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# Copia o arquivo de rerements e Instala as dependências
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copa toda a aplicação
COPY ./env.yaml ./
COPY ./logging.conf ./
COPY ./main.py ./
COPY ./tests/* ./tests/
COPY ./secrets ./secrets
COPY ./bin/* ./bin/
COPY ./embrapadataapi ./embrapadataapi
COPY ./downloads ./downloads

# Define o entrypoint com o FastAPI
ENTRYPOINT ["fastapi", "run", "./main.py"]
