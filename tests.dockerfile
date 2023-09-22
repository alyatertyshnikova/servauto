FROM python:3.9
WORKDIR /servauto_tests
COPY . ./
RUN pip install -r test-requirements.txt
CMD [ "python", "-m", "pytest", "tests/app_tests.py"]