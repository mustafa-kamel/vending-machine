#Build Stage
FROM python:3.8.0-slim as builder

RUN pip install --upgrade pip

RUN apt-get update && apt-get install --no-install-recommends -y && apt-get clean

COPY . /app

WORKDIR /app
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

#App stage
FROM python:3.8.0-slim as app

COPY --from=builder /app/ /opt/vending-machine/
COPY --from=builder /wheels /wheels

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*


WORKDIR /opt/vending-machine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV PORT=8000

RUN chmod +x /opt/vending-machine/startup.sh
CMD ["/opt/vending-machine/startup.sh"]
