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

    resp = {'request_status' : 'success', 'response' : resp}

    return resp

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):

    return jsonify({'request_status' : 'failed', 'errorCode' : 404, 'message' : 'Rota nao implementada'}), 404

@app.errorhandler(500)
def internal_error(e):

    return jsonify({'request_status': 'failed', 'errorCode': 500, 'message': f'Erro interno no servidor: {e}'}), 500

@app.errorhandler(405)
def not_allowed(e):

    return jsonify({'request_status': 'failed', 'errorCode': 405, 'message': f'Metodo nao permitido: {e}'}), 405



def test_form_keys(form):
    chaves_aceitas = {
        'passw' : ['passw', 'password', 'senha'],
        'user' : ['user', 'usuario']
    }

    for key in chaves_aceitas['passw']:

        passw = request.form.get(key, None)
        if passw is not None:
            break
    else:
        chaves_passw = ','.join(chaves_aceitas['passw'])
        message = f'Chave para password deve estar presente. Chaves aceitas {chaves_passw}'
        raise KeyError(message)

    for key in chaves_aceitas['user']:

        user = request.form.get(key, None)
        if user is not None:
            break
    else:
        chaves_passw = ','.join(chaves_aceitas['user'])
        message = f'Chave para usuario deve estar presente. Chaves aceitas {chaves_passw}'
        raise KeyError(message)

    return user, passw



@app.route('/conexao_ldap', methods = ['POST'])
def conexao_ldap():

    try:
        user, passw = test_form_keys(request.form)
    except Exception as e:
        return jsonify({'request_status': 'failed', 'errorCode': 404, 'message': str(e)}), 404

    try:
        teste = teste_connection(user, passw)

        return jsonify(teste), 200
    except Exception as e:
        abort(500, description = str(e))
    


if __name__ == '__main__':
    
    app.run(host = CONFIG_SERVICO['host'], port = CONFIG_SERVICO['port'], debug = True)
    

