import urllib.request,json


base_url = None


def configure_request(app):
    global base_url
    base_url = app.config['QUOTE_API_BASE_URL']

def getquote():
    getquote_url ='http://quotes.stormconsultancy.co.uk/random.json'

    with urllib.request.urlopen(getquote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)



    return get_quote_response