import requests

def validar_ad(user, passw, ip_ldap, porta_ldap):

    url = f'http://{ip_ldap}:{porta_ldap}/conexao_ldap'

    s = requests.Session()
    s.trust_env = False #garante que roda na intranet

    with s.post(url, data = {'user' : user, 'passw' : passw}) as r:

        resposta = r.json()
        assert resposta['request_status'] == 'success'

    return resposta['response']

