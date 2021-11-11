import http.client
from os.path import exists

conn = http.client.HTTPSConnection("alternativeto.net")


def get_data(i):
    if exists(f"data/a-{i:02d}.json"):
        return
    payload = ''
    headers = {
        'Cookie': 'ARRAffinity=9a48c8e43df71fb3995f2e9048cfe59d23c30ee7481f568f359fbe2df65a65ad; ARRAffinitySameSite=9a48c8e43df71fb3995f2e9048cfe59d23c30ee7481f568f359fbe2df65a65ad; ASP.NET_SessionId=sncwnol5nhhbdi0xeftjnajp; a2=656%7Cfalse'
    }
    conn.request(
        "GET", f"/_next/data/vHHdOngKeinV5p94MjmHm/browse/platform/online.json?p={i}&browse=platform&appList=online", payload, headers)
    res = conn.getresponse()
    data = res.read()

    with open(f'./data/a-{i:02d}.json', 'wb') as f:
        f.write(data)

for i in range(1, 500):
    get_data(i)
    print(i)