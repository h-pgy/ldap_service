#mude o nome dessa file para config.py depois de atualizar os dados abaixo!

import socket

def my_ip():

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    return ip

IP_SERVER_LDAP_PREF = 'COLOQUE_O_IP'

CONFIG_SERVICO ={
    'host' : my_ip(), #isso é para pegar o IP do servidor
    'port' : 'A PORTA QUE VOCE DESEJA'
    }