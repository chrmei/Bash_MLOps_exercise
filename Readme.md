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

# install crontab - from project root
crontab scripts/cron.txt

# check
crontab -l

# remove all
crontab -r

tail -f logs/cron.log

sudo systemctl status cron

# note: tests_logs in requirements vs automatically created "tests_logs" directory through pytest files...
