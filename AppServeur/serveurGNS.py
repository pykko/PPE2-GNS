#!/usr/bin/python3
# coding: utf-8


from flask import *
import json
import datetime

from modeles import modeleGNS

app = Flask( __name__ )

@app.route( '/' , methods = [ 'GET' ] )
def accueillir() :
    return make_response( 'GNS' )

@app.route( '/joueurs/connexion/<pseudo>/<mdp>' , methods = [ 'GET' ] )
def seConnecter( pseudo , mdp ) :

    print( pseudo , mdp )

    joueur = modeleGNS.seConnecter( pseudo , mdp )

    print( joueur )

    if joueur !=  None and len( joueur ) != 0 :
        reponse = make_response( json.dumps( joueur ) )
        reponse.mimeType = 'application/json'
        reponse.status_code = 200
    else :
        reponse = make_response( '' )
        reponse.mimeType = 'application/json'
        reponse.status_code = 404

    return reponse


@app.route( '/parties/<idJoueur>/<couleur>' , methods = [ 'POST' ] )
def initier( idJoueur , couleur ) :
    idNouvellePartie = modeleGNS.initier( idJoueur , couleur )
    reponse = make_response( '' )

    if idNouvellePartie != None :
        reponse.headers[ 'Location' ] = '/parties/%d'.format( idNouvellePartie )
        reponse.status_code = 201

    else :
        reponse.status_code = 409

    return reponse
 
 
@app.route( '/parties/<idPartie>/<idJoueur>/<couleur>' , methods = [ 'PUT' ])
def rejoindre(idPartie,idJoueur,couleur):
	idrejoindrePartie = modeleGNS.rejoindre( idPartie , idJoueur , couleur ) 
	reponse = make_response( '' )
	
	if idrejoindrePartie != None :
		reponse.headers[ 'Location' ] = '/parties/%d'.format( idrejoindrePartie )
		reponse.status_code = 202
	
	else :
		reponse.status_code = 406
	
	return reponse

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()



@app.route( '/parties/enattente/<idJoueur>' , methods = [ 'GET' ] )
def getPartiesEnAttenteJoueur( idJoueur ):
	listPartiesEnAttenteJoueur = modeleGNS.partieEnAttenteJoueur(idJoueur)
	
	print (listPartiesEnAttenteJoueur)
	
	if listPartiesEnAttenteJoueur !=  None and len( listPartiesEnAttenteJoueur ) != 0 :
		reponse = make_response( json.dumps( listPartiesEnAttenteJoueur, default = myconverter ) )
		reponse.mimeType = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( 'pas de parties Disponible' )
		reponse.mimeType = 'application/json'
		reponse.status_code = 202

	return reponse
	
	
@app.route( '/joueurs/<idJoueur>/parties/enattente/' , methods = [ 'GET' ])
def getMesPartiesEnAttenteAdversaire( idJoueur ):
	
	listMesPartiesEnAttenteAdversaire = modeleGNS.partieEnAttenteAdversaire(idJoueur)
	
	print (listMesPartiesEnAttenteAdversaire)
	
	if listMesPartiesEnAttenteAdversaire !=  None and len( listMesPartiesEnAttenteAdversaire ) != 0 :
		reponse = make_response( json.dumps( listMesPartiesEnAttenteAdversaire, default = myconverter ) )
		reponse.mimeType = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response(json.dumps( 'pas de parties Disponible') )
		reponse.mimeType = 'application/json'
		reponse.status_code = 202

	return reponse

@app.route( '/joueurs/<idJoueur>/parties/encours/' , methods = [ 'GET' ])
def getMesPartiesEnCours( idJoueur ):
	listMesPartiesEnCours = modeleGNS.partiesEnCours(idJoueur)
	
	print(listMesPartiesEnCours)
	
	if listMesPartiesEnCours !=  None and len( listMesPartiesEnCours ) != 0 :
		reponse = make_response( json.dumps( listMesPartiesEnCours, default = myconverter ) )
		reponse.mimeType = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimeType = 'application/json'
		reponse.status_code = 404

	return reponse
	 
@app.route( '/joueurs/<idJoueur>/parties/terminees/' , methods = [ 'GET' ])
def listPartiesTerminees( idJoueur ):	
	listMesPartiesTerminees = modeleGNS.partiesTerminees(idJoueur)
	
	print(listMesPartiesTerminees)
	
	if listMesPartiesTerminees !=  None and len( listMesPartiesTerminees ) != 0 :
		reponse = make_response( json.dumps( listMesPartiesTerminees, default = myconverter ) )
		reponse.mimeType = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimeType = 'application/json'
		reponse.status_code = 404

	return reponse
	
@app.route( '/parties/<idPartie>' , methods = [ 'GET' ])
def getPartie(idPartie):
	partie = modeleGNS.getPartie(idPartie)
	
	print(partie)
	
	if partie !=  None and len( partie ) != 0 :
		reponse = make_response( json.dumps( partie, default = myconverter ) )
		reponse.mimeType = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimeType = 'application/json'
		reponse.status_code = 404

	return reponse
	
@app.route( '/joueurs/<idJoueur>/parties/<idPartie>' , methods = [ 'PUT' ])
def jouer(idJoueur,idPartie):
	partieJouer = modeleGNS.jouer(idPartie,idJoueur)
	print(partieJouer)
	reponse = make_response( '' )
	
	if partieJouer != None :
		reponse.headers[ 'Location' ] = '/parties/%d'.format( partieJouer )
		reponse.status_code = 202
	
	else :
		reponse.status_code = 406
	
	return reponse


@app.route( '/joueurs/<idJoueur>/parties/<idPartie>/gagner' , methods = [ 'PUT' ])
def gagner( idPartie,idJoueur):
	partiegagner = modeleGNS.gagner( idPartie,idJoueur )
	reponse = make_response( '' )
	
	
	if partiegagner != None :
		reponse.headers[ 'Location' ] = '/parties/%d'.format( partiegagner )
		reponse.status_code = 202
	
	else :
		reponse.status_code = 406
	
	return reponse
	
	
@app.route( '/joueurs/<idJoueur>/parties/<idPartie>/abandonner' , methods = [ 'PUT' ])
def abandonner(idPartie,idJoueur):
	partieAbandonner = modeleGNS.abandonner(idPartie,idJoueur)
	
	reponse = make_response( '' )
	
	
	if partieAbandonner != None :
		reponse.headers[ 'Location' ] = '/parties/%d'.format( partieAbandonner )
		reponse.status_code = 202
	
	else :
		reponse.status_code = 406
	
	return reponse


	
@app.route( '/parties/<idPartie>/annuler' , methods = [ 'PUT' ])
def annuler(idPartie):
	partieAnnuler = modeleGNS.annuler(idPartie)
	
	reponse = make_response( '' )
	
	
	if partieAnnuler != None :
		reponse.headers[ 'Location' ] = '/parties/%d'.format( partieAnnuler )
		reponse.status_code = 202
	
	else :
		reponse.status_code = 406
	
	return reponse	 
	



if __name__ == '__main__' :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )
