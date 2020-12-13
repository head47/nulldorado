CREATE DATABASE nulldorado_data;
CREATE USER djangouser@'10.0.2.2' IDENTIFIED BY 'verysecurepassword';
GRANT ALL ON nulldorado_data.* TO djangouser@'10.0.2.2';
FLUSH PRIVILEGES;
EXIT;
