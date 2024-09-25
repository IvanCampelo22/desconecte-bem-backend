# DESCONECTE BEM

> Status: em andamento 🚀

## Tecnologias usadas

* Python
* Django Rest Framework
* Docker
* Postgres

## Como executar o projeto
1. Ir até a pasta do projeto e criar a virualenv

> virtualenv venv

2. Ative a virtualenv

> source venv/bin/activate

3. Instale as dependencias

> pip install -r requirements.txt

4. Variáveis de ambiente 


> USER_DB=<'USER DO BANCO DE DADOS'>
> HOST_DB=<'HOST DO BANCO DE DADOS'>
> PASSWORD_DB=<'SENHA DO BANCO DE DADOS'>
> NAME_DB=<'NOME DO BANCO DE DADOS'>
> EMAIL_PORT=587
> EMAIL_HOST=<'HOST DO SMTP'>
> EMAIL_HOST_USER=<'EMAIL DO USUÀRIO'>
> EMAIL_HOST_PASSWORD=<'PASSWORD PARA O SMTP GERADO PELO GMAIL>
> EMAIL_BACKEND=<'ENGINE DO BANCO>
> SECRET_KEY=<'SECRET DO DJANGO>
> POSTGRES_NAME=${NAME_DB}
> POSTGRES_USER=${USER_DB}
> POSTGRES_PASSWORD=${PASSWORD_DB}
> POSTGRES_HOST=${HOST_DB}

 
* OBS: 

> As variáveis de ambiente devem estar entre aspas, exceto a porta do banco de dados


5. Vá até a raiz do projeto, onde tem o arquivo manage.py, e inicie o servidor

>  python manage.py runserver

* Teste local

> http://127.0.0.1:8000


## Executando o projeto com Docker

1. Para executar o docker-compose

> docker-compose up 

2. Se quiser construir e subir o container ao mesmo tempo 

> docker-compose up --build

3. Se quiser que o container depois de excutado libere o terminal

> docker-compose up --build -d

4. Construindo e executando o Dockerfile

> sudo docker build -t desconectebem .

> sudo docker run -e USER_DB='user_db' -e PASSWORD_DB='password_db' -e HOST_DB='host_db' -e NAME_DB='name_db' -e PORT_DB='port_db -p 8000:8000 desconectebem



## Como fazer migrações no banco de dados

1. Execute o comando para criar o arquivo na pasta de migrações

> python manage.py makemigrations

2. Depois de criado o arquivo de migração execute o comando para fazer a migração no banco de dados de fato

> python manage.py migrate


## Gerando e usando Tokens

1. Criando super usuário. Com isso o desenvolvedor vai conseguir ter acesso a todos os ambitos do projeto, principalmente a criação de token

> pyhon manage.py createsuperuser
> Insira os dados como email, senha, nome do usuário

2. Gerando token

> No endpoint api/token há dois campos: email e password. Basta inserir os dados que colocou na criação do superusuário
> Irá ser gerado um token de acesso e um token de refresh

<img src="[https://drive.google.com/file/d/16qY6sxAvHnq2YSOXs2hQMDLy-4mdDcMg/view?usp=sharing](https://github.com/charisma-dev/human_analysis_team/assets/64935453/512d9138-13ea-4fa6-80fc-dc7e2a7def67)" width="500"/>

![Captura de tela de 2023-10-27 11-26-54](https://github.com/charisma-dev/human_analysis_team/assets/64935453/945688ad-6d1d-44b6-a447-beb9d878ed74)

3. Usando Token 

> Basta pegar o token de acesso, colocar 'Bearer' como prefixo e em seguida colocar o token

<img src="[https://github.com/charisma-dev/human_analysis_team/assets/64935453/82e1d5d7-4b37-46ac-9077-7a3e69ea32cc)" width="500"/>

![Captura de tela de 2023-10-27 11-53-18](https://github.com/charisma-dev/human_analysis_team/assets/64935453/1dc60fb5-7cf1-4dbf-a77a-8a9c189400c3)

4. Refresh Token 

> Como já foi dito, na hora da criação do token, é gerado um de acesso e um refresh

> No endpoint api/token/refresh deve ser passado o token de refresh para poder ser gerado um novo token de acesso

<img src="[https://github.com/charisma-dev/human_analysis_team/assets/64935453/82e1d5d7-4b37-46ac-9077-7a3e69ea32cc)" width="500"/>

![Captura de tela de 2023-10-27 12-05-01](https://github.com/charisma-dev/human_analysis_team/assets/64935453/56bae028-3c2d-4d6b-8724-f69315b1efe3)

5. Propriedades do token

> 'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),

> 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  
    
> 'SLIDING_TOKEN_LIFETIME': timedelta(days=7), 

> 'SLIDING_TOKEN_REFRESH_TIMEOUT': timedelta(days=14),
    
> 'SLIDING_TOKEN_REFRESH_LIFETIME_RENEWAL': True,


## Trabalhando com Redis e Celery

1. Depois de fazer a instalação do servidor redis, inicie-o

> sudo service redis-server start

2. Execute o celery beat

> celery -A rao beat -l info

3. Execute o Celery

> celery -A rao worker --loglevel=info



