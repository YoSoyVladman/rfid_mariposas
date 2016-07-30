import requests
Z = 1
E = 3
URL = 'http://papalote.cocoplan.mx/v0/'

rfid = 3301411

data = {'rfid':rfid}
url_g = 'historial'
r = requests.get(URL + url_g, params = data);

if r.status_code == requests.codes.ok:
    json  = r.json()
    h = json.get('historial')
    print h
    if(str(E) not in h):
        print 'Entraste zona ' + str(E)
        url_v = 'visitante'
        data_v = {'rfid':rfid,'experiencia':E,'zona':Z}
        rv  = requests.get(URL + url_v, params = data_v)
    else:
        print 'Ya entraste'

else:
    print 'NotFound'
