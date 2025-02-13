import requests


class SocialMediaProxy:
    authorization = None

    def __init__(self, authorization):
        self.authorization = authorization

    def get_general_ads(self, summary=False):
        try:
            platforms = self._get_platforms()
            platforms = [p.get('value') for p in platforms]

            all_fields_names = ['Platform', 'Account', ]
            for platform in platforms:
                fields = self._get_fields(platform)
                for field in fields:
                    if field.get('text') not in all_fields_names:
                        all_fields_names.append(field.get('text'))

            platform_ads_insights = [all_fields_names, ]
            for platform in platforms:
                platform_insights = self.get_platform_ads(platform, summary)
                headers = platform_insights[0]

                insights = []
                for row in platform_insights[1:]:
                    row_dict = dict(zip(headers, row))
                    if 'Cost Per Click' not in headers:
                        row_dict['Cost Per Click'] = round(row_dict['Spend'] / row_dict['Clicks'], 3)
                    new_row = [row_dict.get(column, None) for column in all_fields_names]
                    insights.append(new_row)

                if summary:
                    new_insights = {'Platform': platform, }
                    for i, field in enumerate(all_fields_names):
                        if type(insights[1][i]) in [int, float]:
                            new_insights[field] = sum([row[i] for row in insights[1:]])
                    new_insights['Cost Per Click'] = round(new_insights['Spend'] / new_insights['Clicks'], 3)
                    new_insights = [new_insights.get(column, None) for column in all_fields_names]
                    insights = [new_insights, ]

                platform_ads_insights.extend(insights)

            return platform_ads_insights

        except Exception as e:
            raise Exception(f'Error getting ads: {e}')

    def get_platform_ads(self, platform, summary=False):
        try:
            platforms = self._get_platforms()
            if platform not in [p.get('value') for p in platforms]:
                raise Exception('Platform not found')

            accounts = self._get_accounts(platform)
            fields = {field.get('value'): field.get('text') for field in self._get_fields(platform)}

            platform_ads_insights = [['Platform', 'Account', *fields.values()], ]
            for account in accounts:
                platform_ads_insights.extend(self._get_account_insights(platform, account, fields.keys(), summary))

            return platform_ads_insights

        except Exception as e:
            raise Exception(f'Error getting ads from platform {platform}: {e}')

    def _get_account_insights(self, platform, account, fields, summary=False):
        account_insights = []
        insights = self._get_insights(platform, account.get('id'), account.get('token'), fields)
        for insight in insights:
            account_insights.append([platform, account.get('name'), *[insight.get(key) for key in fields]])

        if summary:
            new_account_insights = [platform, account.get('name'), *([None] * len(fields))]
            for i in range(2, len(fields) + 2):
                if type(account_insights[0][i]) in [int, float]:
                    new_account_insights[i] = sum([row[i] for row in account_insights])
            account_insights = [new_account_insights, ]
        return account_insights

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

    # print(social_media_proxy.get_platform_ads('meta_ads', True))
    print(social_media_proxy.get_general_ads(True))
