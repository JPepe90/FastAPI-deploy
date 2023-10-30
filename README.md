---
title: FastAPI
description: A FastAPI server
tags:
  - fastapi
  - hypercorn
  - python
---

# FastAPI Example

This example starts up a [FastAPI](https://fastapi.tiangolo.com/) server.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-NvLj4?referralCode=CRJ8FE)
## ✨ Features

- FastAPI
- [Hypercorn](https://hypercorn.readthedocs.io/)
- Python 3

## 💁‍♀️ How to use

- Clone locally and install packages with pip using `pip install -r requirements.txt`
- Run locally using `hypercorn main:app --reload`

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- To learn about Hypercorn and how to configure it, read their [Documentation](https://hypercorn.readthedocs.io/)

# python-fastapi-sqlalchemy

Python API for movies using FastAPI and SQLAlchemy. To access the docs with the explanation of the full CRUD go to:

https://fastapi-production-906c.up.railway.app/docs

## Instructions 

To run the code locally, follow this steps:

- Clone the repo
- Create a Virtual Environment
- Activate the V. Environment
- Install modules in requirements.txt

Here are the commands:

```sh
git clone
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
```

Antes de correr la app hay que crear el archivo config_info.py (se deja en el repositorio el archivo config_info.example.py como modelo). Allí se deberá definir la variable my_secret_jwt necesaria para codificar las pw de autenticacion. Tambien se armo un array de usuarios a fines practicos para las pruebas de login.

Una vez generado el archivo se puede inicializar la app con la siguiente instruccion:

```sh
uvicorn main:app --reload --port 5000 --host 0.0.0.0
```