# e_commerce
###### prueba tecnica de creacion de dos microservicios para un e_commerce


# Instalación del Proyecto

# 1. Clonar el Repositorio

Primero, clona el repositorio en tu máquina local:

[E_commerce](https://github.com/sneidermendoza/e_commerce.git)

## 2. Estructura del Proyecto
~~~
e_commerce/
│
├── OrdesServices/
│   ├── api/
│   ├── ordes/
│   ├── venv/
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── ProductServices/
│   ├── api/
│   ├── product/
│   ├── venv/
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── .gitattributes
├── readme.md
└── docker-compose.yml
~~~

# Configuración de la Base de Datos

Tienes dos opciones: usar la base de datos configurada por defecto que está en la nube y ya está poblada con datos de productos y órdenes, o configurar una base de datos local.

#### Opción 1: 
Usar la Base de Datos en la Nube
La base de datos por defecto ya está configurada y contiene datos de productos y órdenes. No necesitas hacer ningún cambio adicional para utilizarla.

#### Opción 2: 
###### Configurar una Base de Datos Local
Si decides configurar una base de datos local, sigue estos pasos:

Abre el archivo settings.py en la carpeta raíz de cada proyecto (ProductServices y OrdesServices).
Configura las variables de la base de datos como se muestra a continuación:
~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'root',
        'PASSWORD': 'sINJImiALwjhwJhqxHmlCJeChrdcDDUa',
        'HOST': 'viaduct.proxy.rlwy.net',
        'PORT': '22041',
    }
}
~~~

Abre dos terminales, una para cada proyecto (ProductServices y OrdesServices), y navega a la carpeta raíz de cada proyecto.

Ejecuta las migraciones en cada proyecto:
## En la terminal de ProductServices
~~~
python manage.py makemigrations
python manage.py migrate
~~~
## En la terminal de OrdesServices
~~~
python manage.py makemigrations
python manage.py migrate
~~~

# 4. Ejecución del Proyecto
Tienes dos opciones para ejecutar el proyecto: manualmente usando entornos virtuales o utilizando Docker.

## Opción 1: Ejecutar Manualmente
Activa el entorno virtual y ejecuta los requisitos:
#### En la terminal de ProductServices
~~~
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8000
~~~
# En la terminal de OrdesServices
~~~
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8001
~~~

## Opción 2: Utilizar Docker
Asegúrate de tener Docker instalado y ejecutando.
Navega a la raíz del proyecto (e_commerce) y ejecuta el siguiente comando:
~~~
docker-compose up --build
~~~

Esto construirá las imágenes Docker y levantará los contenedores. Las aplicaciones estarán disponibles en los siguientes puertos:

OrdesServices en http://localhost:8000
--------------------------------------------
ProductServices en http://localhost:8001
-----------------------------------------
# 5. Acceso a la Documentación de la API
Una vez que las aplicaciones estén en funcionamiento, puedes acceder a la documentación de Swagger en los siguientes enlaces:

OrdesServices: http://localhost:8000
--------------------------------------------
ProductServices: http://localhost:8001
--------------------------------------------
En estas interfaces, podrás utilizar todas las APIs creadas, incluyendo las operaciones para crear, listar, editar y eliminar productos y órdenes.

> [!WARNING]
> Excepción en OrdesServices

En OrdesServices, hay una API especial en la ruta /ordes/create_order_from_array/ que requiere una estructura específica para crear una orden:
{
  "products": [
    {"product_id": int, "quantity": int},
    {"product_id": int, "quantity": int},
    {"product_id": int, "quantity": int}
  ]
}


¡Gracias por usar este proyecto! Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en el repositorio.