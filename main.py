import sys
from client import create_client_app
from server import create_server_app

if __name__ == '__main__':
    app_type = sys.argv[1]
    if app_type == 'client':
        create_client_app()
    elif app_type == 'server':
        create_server_app()
    else:
        print('should write the app type: server or client')
