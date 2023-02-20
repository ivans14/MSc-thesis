import time

from test.generated import Client

def main():
    certificate_authority = open("ca.pem", "rb").read()
    client = Client("127.0.0.1", 50052, root_certs=certificate_authority)

    print("hello")

    # get current value
    connection_status = client.ConnectionController.ConnectionStatus.get()
    print("Connection status:", connection_status)

    # subscribe to value updates
    connection_subscription = client.ConnectionController.ConnectionStatus.subscribe()

    # print every new value
    print("Print new values:")
    connection_subscription.add_callback(print)

    # wait
    time.sleep(3)

    # subscriptions stay active until it is explicitly cancelled:
    connection_subscription.cancel()
    print("Cancelled subscription")

    # received values are iterable:
    print("All received values:", list(connection_subscription))


if __name__ == "__main__":
    main()
