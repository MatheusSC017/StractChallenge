from flask.blueprints import Blueprint
from flask import Response, current_app
from .utils import convert_csv


clients = Blueprint('clients', __name__, template_folder='templates')


@clients.route('/', methods=('GET', ))
def index():
    data = [
        ['Name', 'E-mail', 'Linkedin'],
        ['Matheus Simão Caixeta', 'matheussimao2101@gmail.com', 'https://www.linkedin.com/in/matheussimaocaixeta/']
    ]

    return Response(
        convert_csv(data),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=profile.csv"}
    )


@clients.route('/<platform>/', methods=('GET', ))
def platform(platform):
    api_proxy = current_app.config['API_PROXY']

    platform_ads_insights = api_proxy.get_platform_ads(platform)

    return Response(
        convert_csv(platform_ads_insights),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=platform_ads_insights.csv"}
    )


@clients.route('/<platform>/resumo', methods=('GET', ))
def platform_summary(platform):
    api_proxy = current_app.config['API_PROXY']

    platform_ads_summary = api_proxy.get_platform_ads(platform, True)

    return Response(
        convert_csv(platform_ads_summary),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=platform_ads_summary.csv"}
    )


@clients.route('/geral/', methods=('GET', ))
def general():
    api_proxy = current_app.config['API_PROXY']

    platform_ads_insights = api_proxy.get_general_ads()

    return Response(
        convert_csv(platform_ads_insights),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=platform_ads_general.csv"}
    )


@clients.route('/geral/resumo', methods=('GET', ))
def general_summary():
    api_proxy = current_app.config['API_PROXY']

    platform_ads_summary = api_proxy.get_general_ads(True)

    return Response(
        convert_csv(platform_ads_summary),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=platform_ads_general_summary.csv"}
    )
