## Docker commands
### Development database
To the project integrated PostgreSQL db container. To build development database image use:
```bash
docker compose up -d dev_db_local
```
> *database loads on ports - 15432:5432 

Also you can use pgAdmin with dev database:
```bash
docker compose up -d pg_admin_local
```
> *pgAdmin loads on http://localhost:5050
### Backend container
To build backend app image and container use:
```bash
docker compose up -d dev_backend_local
```
> *development backend container loads on http://localhost:5000/api-ui
### Frontend container
Use this command to build frontend container
```bash
docker compose up -d dev_frontend_local
```
> *development frontend container loads on http://localhost:3000
