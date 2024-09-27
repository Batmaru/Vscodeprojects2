FROM python:3.10-alpine
ADD server.py .
ADD requirements.txt  .
RUN pip install -r requirements.txt
RUN mkdir ./templates
ADD ./templates/index.html ./templates
ADD ./templates/index.html ./templates
CMD ["python","./server.py"]