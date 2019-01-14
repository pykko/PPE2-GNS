#!/usr/bin/python3
# coding: utf-8


from flask import *
import json

from modeles import modeleGNS

app = Flask( __name__ )

@app.route( '/' , methods = [ 'GET' ] )
def accueillir() :
    return make_response( 'XDQ' )

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



if __name__ == '__main__' :
    app.run( debug = True , host = '0.0.0.0' , port = 5000 )


