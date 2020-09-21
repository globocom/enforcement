FROM mc706/pipenv-3.8
LABEL maintainer="globo.com"

COPY . /src/enforcement-service
WORKDIR /src/enforcement-service

RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "main.py"]