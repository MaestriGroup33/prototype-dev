##### use TODO: para documentar o que fizer #####

# Maestri.app

Conectando vidas com inovação, nosso app é uma ponte de oportunidades, onde sonhos se encontram com a realidade.

## Requisitos

- Hatch
- Docker
- npm

## Instruções de Configuração

### 1. Clonando o Repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-diretorio-clonado>
```

### 2. Instalando Dependências

```bash
npm install
```

### 3. Ativando o Ambiente Virtual

```bash
hatch shell
```

### 4. Configuração do Ambiente de Desenvolvimento

```bash
export COMPOSE_FILE=local.yml
docker compose build
docker compose up
```

### 5. Desenvolvendo o Frontend

Para compilar o Tailwind CSS em tempo real:

```bash
npx tailwindcss -i ./src/static/css/input.css -o ./src/static/css/output.css --watch
```

### 6. Referenciando JS com npm

Se necessário, instale as dependências JavaScript via npm:

```bash
npm install htmx
```

Crie um link simbólico para htmx (exemplo):

```bash
ln -s ../../../node_modules/htmx src/static/vendor/htmx
```

### 7. Configurando no Template `base.html`

Adicione a referência ao `htmx` no seu arquivo `base.html`:

```html
<script src="{% static 'vendor/htmx/htmx.min.js' %}"></script>
```

### 8. Badges de Construção

Adicione os seguintes badges ao seu README ou página inicial:

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Comandos Básicos

### Criando Usuários

- Para criar uma **conta de usuário normal**:

  Vá para a página de inscrição e preencha o formulário. Depois de enviar, você verá uma página de "Verificação de E-mail". No console, copie o link de verificação e abra no navegador.

- Para criar uma **conta de superusuário**:

  ```bash
  python manage.py createsuperuser
  ```

### Checagem de Tipos

Para executar checagens de tipo com `mypy`:

```bash
mypy src
```

### Cobertura de Testes

Para rodar os testes, verificar a cobertura e gerar um relatório HTML:

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```

### Executando Testes com `pytest`

```bash
pytest
```

### Live Reloading e Compilação SASS

Consulte a [documentação de Live reloading e SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

Para rodar um worker do Celery:

```bash
cd src
celery -A config.celery_app worker -l info
```

Para rodar tarefas periódicas, inicie o beat scheduler service:

```bash
cd src
celery -A config.celery_app beat
```

Ou embute o serviço beat dentro de um worker (não recomendado para produção):

```bash
cd src
celery -A config.celery_app worker -B -l info
```

### Servidor de E-mail

Para ver os e-mails enviados durante o desenvolvimento, o SMTP local `Mailpit` está disponível como um container Docker.

Acesse `http://localhost:8025` para visualizar as mensagens.

### Sentry

Para configurar o Sentry, você precisa definir a URL DSN no ambiente de produção.

## Deploy

Para detalhes sobre como fazer o deploy, consulte a [documentação de Docker do cookiecutter-django](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
