# Программное средство хранение базы материальных ценностей 

### Описание

Серверная часть программного средства реализована на Django 3.0. Хранение данных реализовано в СУБД MongoDB. Клиентская часть реализована на Vue.js 2.9. Взаимодействие клиентской и серверной частей осуществляется посредством Rest API.

На данный момент реализованы следующие функции:

- просмотр базы материальных ценностей
- добавление записи в базу материальных ценностей
- редактирование записи в базе
- удаление записи из базы
- групповое удаление записей из базы

### Развертывание

Как docker-compose:

- ```
  git clone https://gitwork.ru/van4ester/inventorybase.git
  ```

- ```
  cd inventorybase
  ```

- ```
  docker-compose build
  ```

- ```
  docker-compose up -d
  ```

http://localhost:8080/#/items — клиент