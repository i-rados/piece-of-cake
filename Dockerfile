FROM python:3.10.5
WORKDIR app/
COPY requirements.txt req.txt
RUN pip3 install -r req.txt
COPY . .
EXPOSE 3001
CMD ["python3","app.py"]