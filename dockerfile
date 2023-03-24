FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/cims

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000
