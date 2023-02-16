"""
WSGI config for NN_SiLA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import threading

from django.core.wsgi import get_wsgi_application

from server import Server
from NN_SiLA.example_server.unobservable_command import main

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NN_SiLA.settings')

application = get_wsgi_application()
server = Server(server_uuid=None)
# ca_export_file = 'ca.pem'
# if ca_export_file is not None:
#     with open(ca_export_file, "wb") as fp:
#         fp.write(server.generated_ca)
def run_server():
    server.start_insecure("127.0.0.1",50052)

# Start the server in a separate thread
# server_thread = threading.Thread(target=run_server)
# server_thread.start()

# Call the main function in the main thread
print("calling client")
# client_thread = threading.Thread(target=main)
# client_thread.start()
# main()
print("render")
# application = get_wsgi_application()




