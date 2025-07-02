-- Cria e usa o Banco
CREATE DATABASE agenda_db; 
USE agenda_db; 
-- Cria tabela 
CREATE TABLE contatos (
id_contato INT AUTO_INCREMENT PRIMARY KEY,
nome_contato VARCHAR(50) NOT NULL,
telefone_contato VARCHAR(30) NOT NULL,
email_contato VARCHAR(50) -- Optei por deixar opcional
);

SELECT * FROM contatos;