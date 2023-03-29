FROM python:3.10

COPY . /backend
WORKDIR /.

RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache -r backend/requirements/production.txt


ENTRYPOINT ["sh", "backend/start.sh"]

