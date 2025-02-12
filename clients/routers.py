from flask.blueprints import Blueprint
from flask import render_template

clients = Blueprint('clients', __name__, template_folder='templates')


@clients.route('/', methods=('GET', ))
def index():
    return render_template('index.html')


@clients.route('<int:id>/', methods=('GET', ))
def plataform():
    return render_template('index.html')


@clients.route('<int:id>/resumo', methods=('GET', ))
def plataform_summary():
    return render_template('index.html')



@clients.route('geral/', methods=('GET', ))
def general():
    return render_template('index.html')



@clients.route('geral/resumo', methods=('GET', ))
def general_summary():
    return render_template('index.html')
