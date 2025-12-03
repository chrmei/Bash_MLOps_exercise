# install dev dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv sync
# optional dev
uv pip install -r pyproject.toml --extra dev

# run api
chmod +x api
./api &