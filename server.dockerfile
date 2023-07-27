FROM python:3.9
WORKDIR /servauto
COPY . ./
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python", "app.py"]