
Для создания базы в PostgreSQL(9.1)
$: sudo -i
$: su -l postgres
$: psql
$: create role chess login password "chess';
$: create database chess_test with owner=chess;

