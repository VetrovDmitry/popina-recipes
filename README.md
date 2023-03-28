## Docker commands
### Development database
To the project integrated PostgreSQL db container. To build development database image use:
```bash
docker-compose up -d dev_db_local
```
> *database loads on ports - 15432:5432 

Also you can use pgAdmin with dev database(email: admin@mail.com, psw: adminadmin):
```bash
docker-compose up -d pg_admin_local
```
> *pgAdmin loads on ports - 5050:80
### Backend container
To build backend app image and container use:
```bash
docker-compose up -d dev_backend_local
```
> *development backend container loads on port - 5000