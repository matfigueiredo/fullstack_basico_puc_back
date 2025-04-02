.PHONY: setup run test clean lint migrate seed

PYTHON = python
PIP = pip
FLASK = flask
APP = app.py
DB_FILE = boostme.db

setup:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(APP)

test:
	pytest

clean:
	rm -f $(DB_FILE)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .
	black --check .

init-db:
	$(PYTHON) -c "from app import create_app; from database_manager import DatabaseManager; app = create_app(); with app.app_context(): app.db.init_db()"


seed:
	$(PYTHON) -c "from app import create_app; from database_manager import DatabaseManager; app = create_app(); with app.app_context(): app.db.seed_db()"

dev:
	DEBUG=True $(PYTHON) $(APP)

dev-setup:
	$(PIP) install -r requirements.txt
	$(PIP) install pytest flake8 black

help:
	@echo "Comandos disponíveis:"
	@echo "  setup      - Instalar dependências"
	@echo "  run        - Executar a aplicação"
	@echo "  test       - Executar testes"
	@echo "  clean      - Limpar arquivos temporários e banco de dados"
	@echo "  lint       - Verificar qualidade do código"
	@echo "  init-db    - Inicializar banco de dados"
	@echo "  seed       - Popular banco de dados com dados iniciais"
	@echo "  dev        - Executar em modo de desenvolvimento"
	@echo "  dev-setup  - Instalar dependências de desenvolvimento"
