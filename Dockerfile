FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=project.settings


WORKDIR /app

COPY requirements.txt  /app/
# RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install -r requirements.txt

COPY .  /app/

RUN mkdir -p /app/media
RUN mkdir -p /app/staticfiles
RUN chmod +x /app/manage.py

EXPOSE 8000

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application" ]



