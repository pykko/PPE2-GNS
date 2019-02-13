drop database if exists gns ;

create database if not exists gns default character set utf8 default collate utf8_general_ci ;
use gns ;


create table Joueur (
	id int not null auto_increment ,
	nom varchar( 20 ) not null ,
	mdp varchar( 20 ) not null ,
	email varchar( 40 ) ,
	primary key( id )
	
) engine=InnoDB default charset=utf8 ;

insert into Joueur( nom , mdp ) values ( 'nitharsan' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'tsashua' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'megane' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'vinoth' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'leonard' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'gautier' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'romain' , 'azerty' ) ;
insert into Joueur( nom , mdp ) values ( 'nicolas' , 'azerty' ) ;


create table Partie (
	id int not null auto_increment ,
	creation datetime not null ,
	initiateur int not null ,
	adversaire int ,
	vainqueur int ,
	attendu int ,
	primary key( id ) ,
	foreign key( initiateur ) references Joueur( id ) ,
	foreign key( adversaire ) references Joueur( id ) ,
	foreign key( vainqueur ) references Joueur( id ) ,
	foreign key( attendu) references Joueur( id )
	
) engine=InnoDB default charset=utf8 ; 


create table Choisir (
	id_partie int not null ,
	id_joueur int not null ,
	couleur char( 1 ) not null ,
	primary key( id_partie , id_joueur ) ,
	foreign key( id_partie ) references Partie( id ) ,
	foreign key( id_joueur ) references Joueur( id )

) engine=InnoDB default charset=utf8 ; 

create table Animal(
	numero int not null,
	nom varchar(15) not null,
	primary key ( numero )
	
) engine=InnoDB default charset=utf8 ;

insert into Animal(numero,nom) values(1,'Rat');
insert into Animal(numero,nom) values(2,'Chat');
insert into Animal(numero,nom) values(3,'Loup');
insert into Animal(numero,nom) values(4,'Chien');
insert into Animal(numero,nom) values(5,'Panthère');
insert into Animal(numero,nom) values(6,'Tigre');
insert into Animal(numero,nom) values(7,'Lion');
insert into Animal(numero,nom) values(8,'Eléphant');




create table Pion (
	id_partie int not null ,
	id_pion int not null ,
	couleur char( 1 ) not null ,
	ligne int not null,
	colonne int not null,
	primary key( id_partie , id_pion , couleur ) ,
	foreign key( id_partie ) references Partie( id ),
	foreign key( id_pion ) references Animal( numero ) 

) engine=InnoDB default charset=utf8 ; 






