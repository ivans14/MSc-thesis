from sila2_example_server import Client


def main():
    certificate_authority = open("ca.pem", "rb").read()
    client = Client("127.0.0.1", 50052, insecure = True)
    # command parameters can be specified as positional or keyword arguments:
    response1 = client.GreetingProvider.SayHello("World")
    # commands can have multiple responses, so they return a NamedTuple with one field per response.
    # the command GreetingProvider.SayHello has one response called 'Greeting':
    greeting1 = response1.Greeting


    print(f"Server says '{greeting1}'")
    del client


