# Embrapa Data API
API de acesso aos dados de Viniviticultura da Embrapa. Esta API utiliza os dados dos CSVs disponíveis no site da Embrapa, isso é feito com um intervalo de tempo definido no arquivo de configuração **env.yaml**.

## Instalação
### Pre-Requisitos
- git
- docker
- make
- python >= 3.9 
- virtualenv
- chrome

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
Criando, ativando e executando o projeto com um virtualenv.
```bash
virtualenv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
fastapi dev main.py
```
Será necessário um ambiente com o Google Chrome instalado. Caso você esteja usando WSL2 é possível instalar o chrome pela linha de comando.
```shell
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
```

## Acessando a API
http://localhost:8000