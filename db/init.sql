create user shop_admin password 'admin_password';

create database shop_api_db encoding 'utf-8';
grant all privileges on database shop_api_db to shop_admin;
alter database shop_api_db owner to shop_admin;

create database shop_api_test_db encoding 'utf-8';
grant all privileges on database shop_api_test_db to shop_admin;
alter database shop_api_test_db owner to shop_admin;
