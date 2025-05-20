# Projeto Formativo 

Projeto formativo desenvolvido na máteria de Backend, para o Senai 'Roberto Mange'. 
O projeto faz parte de um sistema de gerenciamento escolar, sendo o backend do projeto, 
onde todo processamento e regras de negócio é desenvolvida. Este projeto foi desenvolvindo usando ```Django RestFramework```

# Como iniciar o projeto? 🤔

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

Para rodar o projeto é necessário ter instalado: 
- [Python 3.9+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/windows/installer/8.0.html)
- API CLIENT como: [Postman](https://www.postman.com/downloads/), [Insominia](https://insomnia.rest/download) ou [Bruno](https://www.usebruno.com/)
### 🔧 Instalação

Para instalar o projeto localmente, use: 

```git clone https://github.com/RaelMorais/formativo_senai.git```


# ⚙️ Configurando o Ambiente Virtual

Navegue até a pasta do projeto e crie um ambiente virtual usando: 

```python -m venv .env```

E então instale os requirements usando 

```pip install -r requirements.txt```

### 🦾🧠 Configuração do Projeto 

Em ```setting.py``` coloque a senha do seu úsuario do WorkBench em **DATABASES**

````python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'formativo_dorival',
        'USER': '#', # Usuario Workbench 
        'PASSWORD': '#', # Senha Workbench 
        'HOST': 'localhost',  # Mysql IP
        'PORT': '3306',  # Porta Mysql      
    }
}
````

⚠️ Importante: O banco **formativo** deve existir no MySQL. Você pode criá-lo manualmente no MySQL Workbench com:

````mysql
    DROP DATABASE IF EXISTS formativo;
    CREATE DATABASE formativo;
    USE formativo;
````
# 🧱 Aplicando Migrações

Para rodar o projeto primeiro é necessário fazer as migrações com: 

```python manage.py makemigrations```

Depois para aplicar as migrações com o banco, rode:

```pythpn manage.py migrate```

E então será necessário criar um superusuario com:

```python manage.py createsuperuser``` e defina o cargo como 'D'. 

# ▶️ Rodando o projeto 

Para rodar o projeto, use ```python manage.py runserver```

# Exemplos de uso

Abaixo será mostrado dois exemplos de uso dos endpoints. 

# Obtendo o token de autenticação: 

Após criar o superusuario no **[passo](#-Aplicando Migrações)**

No Postman ou API CLIENT de sua preferencia, e após executar o projeto **[com](#-Rodando o projeto )**, 
faça uma request com ```http://127.0.0.1:8000/token/``` e no corpo da requisição (request > body > raw)
coloque:

````json
{
    "username":"nome_do_seu_superuser",
    "password":"senha_super_user", 
}

````

E então use o token de ```access```

# Exemplo Request 

1. Criando Usuário

Na URL ```http://127.0.0.1:8000/criar/usuario/``` e em Auth, escolha **Bearer Token** e cole o token Access. 

**modelo de request em raw**

```json
{
  "username": "joaosilva",
  "password": "senha123",
  "email": "joao@email.com",
  "telefone": "11999999999",
  "genero": "M",
  "situacao": "Ef",
  "cargo": "P",
  "data_nasc": "1990-05-20T00:00:00Z",
  "data_contra": "2023-01-10T00:00:00Z",
  "ni": "123456"
}
```

Resposta esperada: 

```json
{
    "message": "usuario criado"
}
```

2. Exibindo Usuarios 

Na URL ```http://127.0.0.1:8000/listar/usuarios/``` e em Auth, escolha **Bearer Token** e cole o token Access. 

Resposta esperada: 

```json
[
    {
        "id": 1,
        "last_login": "2025-05-20T10:46:13Z",
        "is_superuser": true,
        "username": "adm",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": true,
        "is_active": true,
        "date_joined": "2025-05-06T11:45:23Z",
        "telefone": null,
        "genero": null,
        "situacao": "Ef",
        "cargo": "D",
        "data_nasc": null,
        "data_contra": null,
        "ni": "00001",
        "groups": [],
        "user_permissions": []
    },
    {
        "id": 3,
        "last_login": null,
        "is_superuser": false,
        "username": "joaosilva",
        "first_name": "",
        "last_name": "",
        "email": "joao@email.com",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2025-05-20T11:35:17.524385Z",
        "telefone": "11999999999",
        "genero": "M",
        "situacao": "Ef",
        "cargo": "P",
        "data_nasc": "1990-05-20T00:00:00Z",
        "data_contra": "2023-01-10T00:00:00Z",
        "ni": "123456",
        "groups": [],
        "user_permissions": []
    }
]
```

Para documentação completa, acesse: 
 ```http://127.0.0.1:8000/swagger/```
ou 
```http://127.0.0.1:8000/redoc/```

Também é possível acessar pelo [Postman](#)

⌨️ com ❤️ por [Israel Santana](https://github.com/RaelMorais) 😊
