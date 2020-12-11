CREATE DATABASE nulldorado_data;
CREATE USER djangouser@localhost IDENTIFIED BY 'verysecurepassword';
GRANT ALL ON nulldorado_data.* TO djangouser@localhost;
FLUSH PRIVILEGES;
EXIT;
