import requests
Z = 1
E = 2
URL = 'http://papalote.cocoplan.mx/v0/'

rfid = 3301411

data = {'rfid':rfid}
url_g = 'historial'
r = requests.get(URL + url_g, params = data);

if r.status_code == requests.codes.ok:
    json  = r.json()
    h = json.get('historial')
    if not h:
        print 'Permitido'
        url_v = 'visitante'
        data_v = {'rfid':rfid,'experiencia':E,'zona':Z}
        rv  = requests.get(URL + url_v, params = data_v)
    else:
        print 'NoPermitido'

else:
    print 'NotFound'
