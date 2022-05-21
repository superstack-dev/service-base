FROM python:3.8-slim
WORKDIR /pyservice
COPY ./example_imp/requirements.txt /pyservice/example_imp/requirements.txt
COPY ./ /pyservice
RUN pip install --upgrade pip
RUN pip install -e .
WORKDIR /pyservice/example_imp
RUN pip install -r /pyservice/example_imp/requirements.txt

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080" ]
