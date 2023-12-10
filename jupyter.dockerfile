FROM jupyter/scipy-notebook:python-3.10.11

COPY requirements.txt requirements.txt
COPY dist/museum_parser-0.0.1-py3-none-any.whl museum_parser-0.0.1-py3-none-any.whl
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt