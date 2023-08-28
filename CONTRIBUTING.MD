# Developer Instructions

Setup virtual environment.
```bash
python -m venv .venv
source .venv/bin/activate
```

Install requirements.
```bash
make init
```

Other make commands
```bash
make format
make lint
make test
make build
make all # runs format, lint, test, and build
```