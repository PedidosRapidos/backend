# backend
Backend de Pedidos Rapidos

# Testing Manual
El proyecto incluye un docker-compose que permite hacer hotreload del servicio.

```shell
docker-compose up
```
Levanta un postgres(localhost:5432), pgadmin (localhost:9999 admin@mail.com:admin) y la app (localhost:8080).
Cualquier modificacion los archivos dentro de la carpeta pedidos_rapidos se recarga automaticamente.


Para bajar el docker y los volumenes montados:
```shell
docker-compose down -v
```
