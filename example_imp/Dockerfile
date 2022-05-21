FROM python:3.8-slim
WORKDIR /service_base
COPY ./example_imp/requirements.txt /service_base/example_imp/requirements.txt
COPY ./ /service_base
RUN pip install --upgrade pip
RUN pip install -e .
WORKDIR /service_base/example_imp
RUN pip install -r /service_base/example_imp/requirements.txt

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080" ]
