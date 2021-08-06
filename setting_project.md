### Развертывание проекта на сервере Ubuntu
##
- **Необходимо обновить пакеты на сервере**
```
sudo apt update && sudo apt upgrade -y
```
- **установить/обновить git**
```
sudo apt install git
```
- **Установить/обновить python**
```
sudo apt install python3
sudo apt install python3-pip
```
- **Установить tesseract**
```
sudo apt install tesseract-ocr
sudo apt-get install tesseract-ocr-eng
sudo apt-get install tesseract-ocr-rus
```
- **Установить библиотеку для корректной работы opencv-python на сервере**
```
sudo apt-get install -y libgl1-mesa-dev
```
- **Установка и настройка postgresql**
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
- **Логинимся под пользователем (postgres). Дальнейшие команды мы будем выполнять под этим пользователем:**
```
sudo su - postgres
psql
```
**Создадим таблицу**
```
CREATE TABLE newtable;
```
- **Создадим новую роль**
```
CREATE ROLE vscale;
```
- **Добавим привилегии новому пользователю**
```
ALTER ROLE vscale CREATEROLE CREATEDB LOGIN;
```
- **Зададим пароль данному пользователю**
```
\password vscale
```
###[более подробная статья по работе с postgresql](https://community.vscale.io/hc/ru/community/posts/209678249-%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-PostgreSQL-%D0%BD%D0%B0-Ubuntu-16-04)