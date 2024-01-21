
def get_extract_items_method(name: str):

    def extract_data(response):
        return response.get('data')

    def extract_default(response):
        return response

    def extract_getnewsforapp(response):
        return response['newsitems']

    api = {
        'appdetails': extract_data,
        'appuserdetails': extract_data,
        'ajaxgetstoretags': extract_default,
        'GetNewsForApp': extract_getnewsforapp
    }

    return api.get(name, lambda x: None)
