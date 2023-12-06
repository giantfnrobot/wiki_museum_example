FROM jupyter/minimal-notebook

COPY ./requirements.txt requirements.txt
COPY ./dist/museum_data_compiler-0.0.1-py3-none-any.whl museum_data_compiler-0.0.1-py3-none-any.whl
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt