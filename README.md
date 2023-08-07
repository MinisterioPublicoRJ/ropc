# ROPM

## Executando o app localmente

Você precisa ter `git`, `docker` e `docker-compose` instalados para rodar esse
projeto. O serviço **PostgreSQL** rodará dentro de um container Docker.

### Criando o ambiente

Na primeira vez, você precisará clonar o repositório, criar os containers e o
super-usuário no Django:

```shell
git clone <repository-url>
cd ropm
cp env.example .env

pip install -r requirements.txt

# Ativar vitualenv utilizado

docker-compose up

python manage.py migrate
python manage.py createsuperuser
```

Caso o comando `docker-compose` dê erro de `Error while loading shared libraries: libz.so.1: failed to map segment from shared object: Operation not permitted`, tente
rodar os seguintes comandos:

```shell
mkdir $HOME/tmp
sudo TMPDIR=$HOME/tmp docker-compose up
```

### Rodando

Para ativar o ambiente já criado, execute:

```shell
cd ropm

# Ativar vitualenv utilizado

python manage.py runserver

```

Em seguida, basta acessar [localhost:8000](http://localhost:8000/) para ver a aplicação.

### Observação

Para buscar algumas informações utilizadas na aplicação (ex.: lista de municípios, bairros, etc), é necessário que a estação de trabalho do desenvolvedor enxergue os bancos internos do MPRJ - ou seja, que tenha acesso à rede interna. Caso contrário, a aplicação pode falhar em algumas telas quando utilizada localmente.
