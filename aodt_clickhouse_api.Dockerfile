FROM python:3.10
WORKDIR /app
ADD . /app
COPY flask_requirement.txt .
RUN pip install -r flask_requirement.txt
RUN test -d ./img || mkdir ./img && chmod -R 777 ./img
COPY . .

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=app.py
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 2980
# CMD ["flask", "run", "--host=0.0.0.0", "--port=2980"]
# CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "12", "-b", "0.0.0.0:2980", "config:app"]