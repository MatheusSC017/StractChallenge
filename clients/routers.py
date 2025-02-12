from flask.blueprints import Blueprint
from flask import render_template, current_app

clients = Blueprint('clients', __name__, template_folder='templates')


@clients.route('/', methods=('GET', ))
def index():
    return render_template('index.html')


@clients.route('/<platform>/', methods=('GET', ))
def platform(platform):
    api_proxy = current_app.config['API_PROXY']

    headers, platform_ads_insights = api_proxy.get_platform_ads(platform)

    return render_template('table.html', headers=headers, values=platform_ads_insights)


@clients.route('/<platform>/resumo', methods=('GET', ))
def platform_summary(platform):
    return render_template('index.html')


@clients.route('/geral/', methods=('GET', ))
def general():
    return render_template('index.html')


@clients.route('/geral/resumo', methods=('GET', ))
def general_summary():
    return render_template('index.html')
