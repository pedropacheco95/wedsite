from flask import session


def generate_ty_contribution_message(person, title=None):
    client = session.get('client')
    return '{person}, muito obrigado pela contribuição!'.format(person=person, title=client.main_title)
