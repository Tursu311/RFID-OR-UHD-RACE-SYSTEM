-- Active: 1683122981369@@127.0.0.1@3306@exampledb

DROP DATABASE IF EXISTS race;
CREATE DATABASE race;

USE race;


--USE of INT gave error of range, so I used BIGINT
CREATE TABLE runners (
uid BIGINT() NOT NULL PRIMARY KEY,
name VARCHAR(30) NOT NULL,
surnames VARCHAR(30) NOT NULL,
);
CREATE TABLE times (
id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
uid BIGINT NOT NULL,
checkpoint_id INT(2) UNSIGNED,
checkpoint_time TIME,
CONSTRAINT FOREIGN KEY fk_dorsal (uid) REFERENCES runners(uid)
);
