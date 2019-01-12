drop database if exists xdq ;

create database if not exists xdq default character set utf8 default collate utf8_general_ci ;
use xdq ;


create table Joueur (
	id int not null auto_increment ,
	nom varchar( 20 ) not null ,
	mdp varchar( 20 ) not null ,
	email varchar( 40 ) ,
	primary key( id )
	
) engine=InnoDB default charset=utf8 ;



create table Partie (
	id int not null auto_increment ,
	creation datetime not null ,
	initiateur int not null ,
	adversaire int ,
	vainqueur int ,
	son_tour int ,
	primary key( id ) ,
	foreign key( initiateur ) references Joueur( id ) ,
	foreign key( adversaire ) references Joueur( id ) ,
	foreign key( vainqueur ) references Joueur( id ) ,
	foreign key( son_tour ) references Joueur( id )
	
) engine=InnoDB default charset=utf8 ; 

create table Choisir (
	id_partie int not null ,
	id_joueur int not null ,
	couleur varchar( 10 ) not null ,
	primary key( id_partie , id_joueur ) ,
	foreign key( id_partie ) references Partie( id ) ,
	foreign key( id_joueur ) references Joueur( id )

) engine=InnoDB default charset=utf8 ; 




