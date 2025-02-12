from flask import current_app
import requests


class SocialMediaProxy:
    authorization = None

    def __init__(self, authorization):
        self.authorization = authorization

    def get_platform_ads(self, platform):
        try:
            platforms = self._get_platforms()
            if platform not in [p.get('value') for p in platforms]:
                raise Exception('Platform not found')

            accounts = self._get_accounts(platform)
            fields = self._get_fields(platform)
            fields_names = [f.get('text') for f in fields]
            fields_keys = [f.get('value') for f in fields]

            platform_ads_insights = []
            for account in accounts:
                insights = self._get_insights(platform, account.get('id'), account.get('token'), fields_keys)
                for insight in insights:
                    platform_ads_insights.append([platform, account.get('name'), *[insight.get(key) for key in fields_keys]])

            headers = ['Platform', 'Ad Name', *fields_names]
            return headers, platform_ads_insights

        except Exception as e:
            raise Exception(f'Error getting ads from platform {platform}: {e}')

    def _get_platforms(self):
        response = requests.get('https://sidebar.stract.to/api/platforms',
                                headers={'Authorization': self.authorization})

        return self._get_content_or_error(response).get('platforms')

    def _get_accounts(self, platform):
        url = f'https://sidebar.stract.to/api/accounts?platform={platform}'
        return self._get_from(url, 'accounts')

    def _get_fields(self, platform):
        url = f'https://sidebar.stract.to/api/fields?platform={platform}'
        return self._get_from(url, 'fields')

    def _get_insights(self, platform, account, token, fields):
        url = f'https://sidebar.stract.to/api/insights?platform={platform}&account={account}&token={token}&fields={",".join(fields)}'
        return self._get_from(url, 'insights')

    def _get_from(self, url, key):
        response = requests.get(url, headers={'Authorization': self.authorization})

        content = self._get_content_or_error(response)
        values = content.get(key)
        if 'pagination' in content.keys():
            for i in range(2, content.get('pagination').get('total') + 1):
                try:
                    response = requests.get(url + f'&page={i}', headers={'Authorization': self.authorization})
                    content = self._get_content_or_error(response)
                    values.extend(content.get(key))
                finally:
                    pass
        return values

    def _get_content_or_error(self, response):
        if response.status_code != 200:
            raise Exception('Error connecting to API')

        content = response.json()

        if 'error' in content.keys():
            raise Exception(f'Error: {content["error"]}')

        return content


if __name__ == '__main__':
    social_media_proxy = SocialMediaProxy('ProcessoSeletivoStract2025')

    print(social_media_proxy.get_platform_ads('meta_ads'))
