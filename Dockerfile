# syntax=docker/dockerfile:1
FROM python:3.9.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

RUN mkdir -p /transformers/hf_model_cache

RUN mkdir -p /transformers/hf_dataset_cache

ENV HF_DATASETS_CACHE=/transformers/hf_dataset_cache
ENV HF_HOME=/transformers

COPY . /code/