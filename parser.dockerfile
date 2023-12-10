FROM python:3.10.13-slim-bullseye

COPY requirements.txt /requirements.txt
COPY dist/museum_parser-0.0.1-py3-none-any.whl /museum_parser-0.0.1-py3-none-any.whl
COPY run_pkg.py /run_pkg.py
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["python", "-u", "-m", "run_pkg"]