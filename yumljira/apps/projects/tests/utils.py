def add_token(client, jwt):
    client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt)
