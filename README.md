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
Para acessar a API basta abrir o endereço abaixo em um navegador.
```
http://localhost:8000
```

Os recursos / (index) e o /docs são públicos e podem ser acessados sem a necessidade de login, já os recursos de dados 
precisam de um token JWT.

### Requisitando um token JWT
Para solicitar um token é necessário realizar um POST em /token passando username e password. A configuração padrão de usuário 
e senha é:
```
username: embrapa
password: embrapa
```
Exemplo de retorno:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWJyYXBhIiwiZXhwIjoxNzIyNDc1NDI2fQ.L7tFD1h3wPAgGkoUolD9H3V50r2BRksrcO1W1AdE_P8",
    "token_type": "bearer"
}
```
Uma vez com o token em mãos, para acessar os recursos que necessitam de autenticação
é preciso enviar o header Authorization com o access token da seguinte forma:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWJyYXBhIiwiZXhwIjoxNzIyNDc1NDI2fQ.L7tFD1h3wPAgGkoUolD9H3V50r2BRksrcO1W1AdE_P8
```
### Filtrando/Paginando os recursos
Para filtrar e paginar um recurso é necessário fazer uso dos parâmetros, **limit**, **skip** e **filters**.
O limit e skip sâo utilizados para paginar assim como em queries SQL. Já os filters é um campo que recebe múltiplos 
filtros separados por vírgula e que executa uma clausa AND entre todos os filtros.

Os filtros permitidos depende de cada recurso e qualquer campo de um registro de recurso pode ser utilizado. Exemplo:
```
http://localhost:8000/production?limit=10&skip=0&filters=year:2023,category:VINHO DE MESA
```

## Configurações
As configurações da aplicação se dividem entre os arquivos **env.yaml**, configurações gerais, e o logging.conf, que são 
as configurações de log.

### env.yaml
Nesse arquivo é possível definir as configurações básicas da aplicação
```yaml
app_config:
  application_name: Embrapa Data API
  database_name: 'embrapa.db'
  auth:
    username: embrapa
    password: <senha em formato de hash>
    secret_key: abcd1234
    algorithm: HS256
    expires_minutes: 30
  jobs:
    - name: embrapa
      params:
        url: http://vitibrasil.cnpuv.embrapa.br/
        downloaded_data_path: ./downloads/embrapa
      module: embrapadataapi.tasks.embrapa_job
      clazz: EmbrapaCrawlJob
      seconds_interval: 120
```

### Gerando um novo hash de senha
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("NOVA SENHA"))
```
Exemplo de saída
```
$2b$12$o3ic6Ypmckujsm1TcLkJI.M2jsDVEcpC0BE0bbceLyMN8l0t.3u1y
```

# Arquitetura
O sistema é dividido entre uma API e um Scheduler que executa jobs de forma assíncrona. Os Jobs são responsáveis por realizar a ingestão dos dados, como um ETL, enquanto a API é responsável por servir esses dados de forma uniforme sob recursos web.

![Arquitetura da API](./docs/images/api_archytecture.jpg "Arquitetura da API")

### Inicialização
Durante o processo de startup os jobs são executados pela primeira vez e, somente ao final dessa execução, é que a API fica disponível para acesso. Se algum erro acontecer durante a execução desses jobs da inicialização, por falha ao acessar o site da embrapa por exemplo, os dados que já estão na pasta de downloads serão utilizados para fazer a ingestão inicial.

Após a conclusão da inicialização, os jobs serão executados em loop respeitando o intervalo de tempo definido no arquivo de configurações.

### Armazenamento
Uma vez que os dados tenham sido capturados do site da Embrapa eles são armazenados em um banco sqlite3. 
Quando uma nova versão dos dados é ingerida, as tabelas que representam cada um dos recursos (Produção, Processamento, 
Comercialização, Importação, Exportação) são subrescritas e a coluna `created_at` representa a data em que os arquivos 
foram escritos no disco.

O banco sqlite é escrito em disco ou memória de acordo com a configuração no arquivo `env.yaml`

# Testes
Rodando os testes localmente
```bash
make test-local
```
Rodando os testes de forma isolada via Docker
```bash
make test-docker
```