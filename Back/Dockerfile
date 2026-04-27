#Usaremos  una imagen base de Python 3.14.3 con Alpine Linux 3.23.
FROM python:3.14.3-alpine3.23

# Estamos estableciendo el directorio de trabajo dentro del contenedor a /app.
WORKDIR /app

# Copiamos el archivo app.py desde el directorio actual (donde se encuentra el Dockerfile) al directorio de trabajo(WORKDIR) dentro del contenedor.
COPY app.py app.py
# ya no se ocupa por el uso del  volumen al momento de hacer el contenedor


# Instalamos Flask, que es un microframework de Python para desarrollar aplicaciones web. Esto se hace utilizando pip, el gestor de paquetes de Python.
RUN pip install flask
RUN pip install flask-cors


# Exponemos el puerto 5000 para que la aplicación Flask pueda ser accesible desde fuera del contenedor.
CMD ["python", "-m", "flask", "--app", "app.py", "run", "--host=0.0.0.0" , "--port=5000"]
