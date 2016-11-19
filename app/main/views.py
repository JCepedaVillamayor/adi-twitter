from flask import Flask, request, redirect, url_for, g, session, flash, render_template
from flask_oauthlib.client import OAuth
from . import main, twitter

@twitter.tokengetter
def get_twitter_token(token=None):
    ''' Obtain token for the current session'''
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@main.before_request
def before_request():
    ''' clean last session to include the new one '''
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@main.route('/')
def index():
    ''' main page '''
    if g.user is not None:
        # Ojo comprobar si hay tweets y pasarlo al html
        print "get tweets"
#        resp = twitter.request(.....

    return render_template('index.html')


@main.route('/login')
def login():
    ''' Get auth token (request) '''
    callback_url=url_for('.oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)

# Eliminar sesion
@main.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('.index'))

# Callback
@main.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('.index'))

@main.route('/op1', methods=['POST'])
def deleteTweet():
    return redirect(url_for('.index'))

@main.route('/op2', methods=['POST'])
def retweet():
    return redirect(url_for('.index'))

@main.route('/op3', methods=['POST'])
def follow():
    return redirect(url_for('.index'))

@main.route('/op4', methods=['POST'])
def tweet():
    # Paso 1: Si no estoy logueado redirigir a pagina de /login
               # Usar g y redirect

    # Paso 2: Obtener los datos a enviar
               # Usar request (form)

    # Paso 3: Construir el request a enviar con los datos del paso 2
               # Utilizar alguno de los metodos de la instancia twitter (post, request, get, ...)

    # Paso 4: Comprobar que todo fue bien (no hubo errores) e informar al usuario
               # La anterior llamada devuelve el response, mirar el estado (status)

    # Paso 5: Redirigir a pagina principal (hecho)
    return redirect(url_for('.index'))
