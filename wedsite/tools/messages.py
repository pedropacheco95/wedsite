from flask import session

def generate_ty_contribution_message(person,title=None):
    client = session.get('client')
    return 'Muito obrigado {person} pela contribuição! Beijinhos, {title}'.format(person=person,title=client.main_title)