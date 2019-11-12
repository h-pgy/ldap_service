from ldap3 import Server, Connection, ALL, NTLM
from flask import Flask, jsonify, request, abort
from config import IP_SERVER_LDAP_PREF, CONFIG_SERVICO


def teste_connection(user, passw):

    user = 'REDE\\{}'.format(user)
    server = Server(IP_SERVER_LDAP_PREF, get_info=ALL)
    conn = Connection(server, user=user, password=passw, authentication=NTLM)
    resp = conn.bind()
    conn.unbind()
    assert conn.closed == True, 'Conexao permaneceu aberta por alguma razao'

    resp = {'request_status' : 'success', 'response' : response}

    return resp

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):

    return jsonify({'request_status' : 'failed', 'errorCode' : 404, 'message' : 'Rota nao implementada'}), 404

@app.errorhandler(500)
def internal_error(e):

    return jsonify({'request_status': 'failed', 'errorCode': 500, 'message': f'Erro interno no servidor: {e}'}), 500

@app.route('/conexao_ldap/', methods = ['POST'])
def conexao_ldap():
    try:
        user = request.form.get('user')
        passw = request.form.get('passw')

        teste = teste_connection(user, passw)

        return jsonify(teste), 200
    except Exception as e:
        abort(500, description = str(e))
    


if __name__ == '__main__':
    
    app.run(host = CONFIG_SERVICO['host'], port = CONFIG_SERVICO['port'], debug = True)
    

