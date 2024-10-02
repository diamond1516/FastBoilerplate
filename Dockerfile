# Python image versiyasini belgilash
FROM python:3.9-slim

# Katalogni o'rnatish
WORKDIR /app

# Requirements faylini konteynerga nusxalash
COPY ./requirements/ requirements/
COPY ./requirements/dev.txt /requirements/dev.txt
COPY ./requirements/base.txt /requirements/base.txt

# Python kutubxonalarini o'rnatish
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/dev.txt

# Barcha loyihani konteynerga nusxalash
COPY . .

# Portni belgilash
EXPOSE 8000

# FastAPI serverni ishga tushirish
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
