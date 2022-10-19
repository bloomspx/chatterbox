FROM python:3.9

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install umap-learn==0.5.1

RUN pip install bertopic

RUN pip install -r requirements.txt

COPY . .

CMD python3 app.py