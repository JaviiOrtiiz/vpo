# Image: python:latest
FROM arm32v7/python:latest

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Copy main.py to the working directory
COPY main.py .

# Copiar el script de shell al contenedor
COPY run.sh .

# Copiar secrets.txt al contenedor
COPY secrets.txt .

# Copiar contenido_previo.html al contenedor
COPY contenido_previo.html .

#Copiar entrypoint.sh al contenedor
COPY entrypoint.sh .

# Install the required packages
RUN pip install -r requirements.txt

# Run the shell script to execute the python script periodically
CMD ["sh", "entrypoint.sh"]