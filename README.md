# FIAP Data API
API de acesso aos dados da ISEB3. Esta API utiliza os dados dos CSVs de respostas das empresas aos questionários da ISEB3.

## Instalação
### Pre-Requisitos
- git
- docker
- make
- python >= 3.9 
- virtualenv


```bash
git clone git@github.com:baliberdin/fiap-data-api.git
```
É recomendado a utilização de um virtualenv ou similar para rodar a API localmente. Também é possível rodar a API diretamente via Docker. Os dois exemplos são exibidos abaixo.

### Rodando via Docker
Rodando a API via docker utilizando as tasks do Makefile.
A task `run` também executa o `build`.
```bash
make run
```

### Rodando local com python/virtualenv
Criando, ativando e executando o projeto com um virtualenv
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

## Acessando a API
http://localhost:8000