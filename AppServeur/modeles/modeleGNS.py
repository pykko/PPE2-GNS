#!/usr/bin/python3
# coding: utf-8


import mysql.connector


connexion = None

global pions
pions = {}
pions['blanc'] = [(3,1),(2,6),(3,5),(2,2),(3,3),(1,7),(1,1),(3,7)]
pions['noir'] = [(7,7),(8,2),(7,3),(8,6),(7,5),(9,1),(9,7),(7,1)]

def getConnexion() :
    global connexion

    try :
        if connexion == None :
            connexion = mysql.connector.connect(
                host = 'localhost' ,
                user = 'root' ,
                password = 'azerty' ,
                database = 'gns'
            )

        return connexion
    except :
        return None


def seConnecter( nom , mdp ) :
    try :
        curseur = getConnexion().cursor()

        requete = '''
            select id , email
            from Joueur
            where nom = %s
            and mdp = %s
        '''

        curseur.execute( requete , ( nom , mdp ) )

        enregistrement = curseur.fetchone()

        joueur = {}

        if enregistrement != None :
            joueur[ 'id' ] = enregistrement[ 0 ]
            joueur[ 'nom' ] = nom
            joueur[ 'email' ] = enregistrement[ 1 ]

        curseur.close()
        return joueur

    except mysql.connector.Error as e :
        print( e )
        return None


def initier( idJoueur , couleur ) :
    try :
        curseur = getConnexion().cursor()

        requetePartie = '''
                insert into Partie( creation , initiateur , attendu )
                values( now() , %s , %s )
            '''

        if couleur == 'B' :
            curseur.execute( requetePartie , ( idJoueur , idJoueur ) )
        else :
            curseur.execute( requetePartie , ( idJoueur, None ) )

        idPartie = curseur.lastrowid

        requeteChoisir = '''
                insert into Choisir
                values( %s , %s , %s )
            '''
        curseur.execute( requeteChoisir , ( idPartie , idJoueur , couleur ) )
        
        pion = initierPions(idPartie , couleur ,curseur)	
        	
        connexion.commit()
        curseur.close()
        return idPartie
        
    except mysql.connector.Error as e :
        print( e )
        return None


def rejoindre(idPartie , idJoueur , couleur):
	try:
		curseur = getConnexion().cursor()
		if couleur == 'B':
			requetePartie = '''
				update Partie
				set adversaire = %s , attendu = %s
				where id = %s
				'''
			curseur.execute( requetePartie, ( idJoueur , idJoueur , idPartie))
		else:
			requetePartie = '''
				update Partie
				set adversaire = %s
				where id = %s
				'''
			curseur.execute( requetePartie, ( idJoueur , idPartie))
		
		
		requeteChoisir = '''
				insert into Choisir
				values( %s , %s , %s )
			'''
		curseur.execute(requeteChoisir ,(idPartie , idJoueur , couleur ) )
		
		pion = initierPions(idPartie , couleur ,curseur)
				
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print( e )
		return None



def initierPions(idPartie, couleur ,curseur):
	try:
		 
		animals = getAnimaux()
		
		for i in range(len(animals)):
			requetePions = ''' 
				insert into Pion 
				values( %s , %s , %s , %s , %s ) 
					'''
			if couleur == 'B':
				curseur.execute( requetePions , ( idPartie ,animals[i]['numero'] , 'B' ,pions['blanc'][i][0] , pions['blanc'][i][1]) )
			else:
				curseur.execute( requetePions , ( idPartie ,animals[i]['numero'] , 'N' ,pions['noir'][i][0] , pions['noir'][i][1]) )
		
		
		return idPartie
				
	except mysql.connector.Error as e :
				print( e )
				return None




def partieEnAttenteJoueur(idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				select p.id, p.creation, initiateur , nom , couleur
				from Choisir c
				inner join Joueur j
				on c.id_joueur = j.id
				inner join Partie p
				on c.id_partie = p.id
				where initiateur != %s
				and adversaire is NULL
			'''
		curseur.execute( requetePartie , (idJoueur, ))
		
		enregistrements = curseur.fetchall()
		
		parties = []
		for unEnregistrement in enregistrements :
			unPartie = {}
			unPartie[ 'idPartie' ] = unEnregistrement[ 0 ]
			unPartie[ 'creation' ] = unEnregistrement[ 1 ]
			unPartie[ 'initiateur' ] = unEnregistrement[ 2 ]
			unPartie[ 'nom' ] = unEnregistrement[ 3 ]
			unPartie[ 'couleur' ] = unEnregistrement[ 4 ]
			parties.append( unPartie )
			
		curseur.close()
		return parties
		
	except mysql.connector.Error as e :
		print(e)
		return None
		

def partieEnAttenteAdversaire( idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				select p.id, p.creation, initiateur , nom , couleur
				from Choisir c
				inner join Joueur j
				on c.id_joueur = j.id
				inner join Partie p
				on c.id_partie = p.id
				where initiateur = %s
				and adversaire is NULL
			'''
		curseur.execute( requetePartie , (idJoueur, ))
		
		enregistrements = curseur.fetchall()
		
		parties = []
		for unEnregistrement in enregistrements :
			unPartie = {}
			unPartie[ 'idPartie' ] = unEnregistrement[ 0 ]
			unPartie[ 'creation' ] = unEnregistrement[ 1 ]
			unPartie[ 'initiateur' ] = unEnregistrement[ 2 ]
			unPartie[ 'nom' ] = unEnregistrement[ 3 ]
			unPartie[ 'couleur' ] = unEnregistrement[ 4 ]
			parties.append( unPartie )
			
		curseur.close()
		return parties
		
	except mysql.connector.Error as e :
		print(e)
		return None

def partiesEnCours(idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				select id, creation, initiateur , 
				(select nom from Joueur where id = initiateur),
				(select couleur from Choisir where id_joueur = initiateur and id_partie = id),
				adversaire ,(select nom from Joueur where id =adversaire),
				(select couleur from Choisir where id_joueur = adversaire and id_partie = id),attendu
				from Partie
				where initiateur is not NULL
				and adversaire is not NULL
				and initiateur = %s 
				or adversaire = %s
			'''
		curseur.execute( requetePartie , (idJoueur,idJoueur ))
		
		enregistrements = curseur.fetchall()
		
		parties = []
		for unEnregistrement in enregistrements :
			unPartie = {}
			unPartie[ 'idPartie' ] = unEnregistrement[ 0 ]
			unPartie[ 'creation' ] = unEnregistrement[ 1 ]
			unPartie[ 'initiateur' ] = unEnregistrement[ 2 ]
			unPartie[ 'nomInitiateur' ] = unEnregistrement[ 3 ]
			unPartie[ 'couleurInitiateur'] = unEnregistrement[ 4 ] 
			unPartie[ 'adversaire' ] = unEnregistrement[ 5 ]
			unPartie[ 'nomAdversaire' ] = unEnregistrement[ 6 ]
			unPartie[ 'couleurAdversaire' ] = unEnregistrement[ 7 ]
			unPartie[ 'Attendu' ] = unEnregistrement[ 8 ]
			
			
			parties.append( unPartie )
			
		curseur.close()
		return parties
		
	except mysql.connector.Error as e :
		print(e)
		return None


def partiesTerminees(idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				select id, creation, initiateur , 
				(select nom from Joueur where id = initiateur),
				(select couleur from Choisir where id_joueur = initiateur and id_partie = id),
				adversaire ,(select nom from Joueur where id =adversaire),
				(select couleur from Choisir where id_joueur = adversaire and id_partie = id),vainqueur
				from Partie
				where initiateur is not NULL
				and adversaire is not NULL 
				and vainqueur is not NULL
				and initiateur = %s 
				or adversaire = %s
			'''	
			
		curseur.execute( requetePartie , (idJoueur,idJoueur))
		
		enregistrements =curseur.fetchall()
		
		parties = []
		
		for unEnregistrement in enregistrements :
			unPartie = {}
			unPartie[ 'idPartie' ] = unEnregistrement[ 0 ]
			unPartie[ 'creation' ] = unEnregistrement[ 1 ]
			unPartie[ 'initiateur' ] = unEnregistrement[ 2 ]
			unPartie[ 'nomInitiateur' ] = unEnregistrement[ 3 ]
			unPartie[ 'couleurInitiateur'] = unEnregistrement[ 4 ] 
			unPartie[ 'adversaire' ] = unEnregistrement[ 5 ]
			unPartie[ 'nomAdversaire' ] = unEnregistrement[ 6 ]
			unPartie[ 'couleurAdversaire' ] = unEnregistrement[ 7 ]
			unPartie[ 'vainqueur' ] = unEnregistrement[ 8 ]
			
			parties.append( unPartie )
		
		curseur.close()
		return parties
	
	except mysql.connector.Error as e:
		print(e)
		return None
		


def getPartie(idPartie):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				select id, creation, initiateur , 
				(select nom from Joueur where id = initiateur),
				(select couleur from Choisir where id_joueur = initiateur and id_partie = id),
				adversaire ,(select nom from Joueur where id =adversaire),
				(select couleur from Choisir where id_joueur = adversaire and id_partie = id),attendu,vainqueur
				from Partie
				where id = %s
			'''	
			
		curseur.execute( requetePartie , (idPartie,))
		
		enregistrement =curseur.fetchone()
		
		
		
		
		unPartie = {}
		
		unPartie[ 'idPartie' ] = idPartie
		unPartie[ 'creation' ] = unEnregistrement[ 1 ]
		unPartie[ 'initiateur' ] = unEnregistrement[ 2 ]
		unPartie[ 'nomInitiateur' ] = unEnregistrement[ 3 ]
		unPartie[ 'couleurInitiateur'] = unEnregistrement[ 4 ] 
		unPartie[ 'adversaire' ] = unEnregistrement[ 5 ]
		unPartie[ 'nomAdversaire' ] = unEnregistrement[ 6 ]
		unPartie[ 'couleurAdversaire' ] = unEnregistrement[ 7 ]
		
		if unEnregistrement[ 8 ] != None:
			unPartie[ 'Attendu' ] = unEnregistrement[ 8 ]
		else:
			unPartie[ 'Attendu' ] = 0
		
		if unEnregistrement[ 9 ] != None:
			unPartie[ 'vainqueur' ] = unEnregistrement[ 9 ]
		else:
			unPartie[ 'vainqueur' ] = 0
		
	
		curseur.close()
		return unPartie
	
	except mysql.connector.Error as e:
		print(e)
		return None
				
				
def jouer(idPartie,idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie1 = '''
				select initiateur,adversaire,attendu
				from Partie
				where id = %s
				'''
		curseur.execute( requetePartie1 , (idPartie,))
		
		enregistrement =curseur.fetchone()
				
		if enregistrement[0] == enregistrement[2]:		
			requetePartie2 = '''
					update Partie
					set attendu = adversaire
					where id = %s
					and attendu = %s
					'''
		else :
			requetePartie2 = '''
					update Partie
					set attendu = initiateur
					where id = %s
					and attendu = %s
					'''
			
		curseur.execute(requetePartie2, ( idPartie , idJoueur))
		
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print( e )
		return None
		

def gagner(idPartie,idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				update Partie
				set attendu = null , vainqueur = %s			
				where id = %s
				'''
		
		curseur.execute(requetePartie, (idJoueur,idPartie))
		
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print( e )
		return None


def abandonner(idPartie,idJoueur):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie1 = '''
				select initiateur,adversaire,attendu
				from Partie
				where id = %s
				'''
		curseur.execute( requetePartie1 , (idPartie,))
		
		enregistrement =curseur.fetchone()
				
		if enregistrement[0] == idJoueur:		
			requetePartie2 = '''
					update Partie
					set attendu = null , vainqueur = adversaire
					where id = %s
					'''
		else :
			requetePartie2 = '''
					update Partie
					set attendu = null , vainqueur = initiateur
					where id = %s
					'''
			
		curseur.execute(requetePartie2, ( idPartie , ))
		
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print( e )
		return None
		
def annuler(idPartie):
	try:
		curseur = getConnexion().cursor()
		
		requetePartie = '''
				update Partie
				set attendu = null , vainqueur = null
				where id = %s
				'''
		curseur.execute(requetePartie, (idPartie,))
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print(e)
		return None
	
def getAnimaux():
	try:
		curseur = getConnexion().cursor()
		
		requeteAnimal = '''
			select numero , nom
			from Animal
			'''
		
		curseur.execute(requeteAnimal,())
		
		enregistrement = curseur.fetchall()
		
		animaux = []
		
		for unenregistrement in enregistrement:
			animal = {}
			animal['numero'] = unenregistrement[0]
			animal['nom'] = unenregistrement[1]
			animaux.append(animal)
			
		curseur.close()
		return animaux
		
	except mysql.connector.Error as e :
		print(e)
		return None
		

def getPionsDansPartie(idPartie):
	try :
		curseur = getConnexion().cursor()
		
		requetePion = '''
			select id_pion,nom,couleur,ligne,colonne
			from Pion p
			inner join Animal a
			on p.id_pion = a.numero
			where id_partie = %s
			'''
		
		curseur.execute(requetePion ,(idPartie, ))
		
		
		enregistrement = curseur.fetchall()
		
		pionPartie = []
		
		for unenregistrement in enregistrement:
			pion = {}
			pion['idpion'] = unenregistrement[0]
			pion['nom'] = unenregistrement[1]
			pion['couleur'] = unenregistrement[2]
			pion['ligne'] = unenregistrement[3]
			pion['colonne'] = unenregistrement[4]
			
			pionPartie.append(pion)
			
		curseur.close()
		return pionPartie
		
	except mysql.connector.Error as e :
		print(e)
		return None
			
			
def deplacerPion(idPartie,numAnimal,couleurAnimal,ligne,colonne):
	try :
		curseur = getConnexion().cursor()
		
		requeteDeplacement = '''
			update Pion
			set ligne = %s , colonne = %s
			where id_partie = %s
			and id_pion = %s
			and couleur = %s
			'''
			
		curseur.execute(requeteDeplacement,(ligne,colonne,idPartie,numAnimal,couleurAnimal))
		
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print(e)
		return None
		
		
def deplacerPionAvecSuppression(idPartie,numAnimal,couleurAnimal,ligne,colonne,adNumAnimal,adCouleurAnimal):
	try :
		curseur = getConnexion().cursor()
		
		requeteSuppression = '''
			delete 
			from Pion
			where id_pion = %s
			and id_partie = %s
			and couleur = %s
			'''
		
		curseur.execute( requeteSuppression ,(adNumAnimal,idPartie,adCouleurAnimal))
		
		requeteDeplacement = '''
			update Pion
			set ligne = %s , colonne = %s
			where id_partie = %s
			and id_pion = %s
			and couleur = %s
			'''
			
		curseur.execute(requeteDeplacement,(ligne,colonne,idPartie,numAnimal,couleurAnimal))
		
		connexion.commit()
		curseur.close()
		return idPartie
		
	except mysql.connector.Error as e :
		print(e)
		return None
		

		
		
			
		
	
