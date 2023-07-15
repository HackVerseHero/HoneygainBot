FROM python:3.10

WORKDIR user/app/honey_pot

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

RUN chmod 777 .

COPY . .

CMD ["python", "bot.py"]