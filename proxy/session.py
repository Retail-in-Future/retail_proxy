from proxy.utils import singleton


class Session(metaclass=singleton):
    def __init__(self):
        self.__subscrption_list = dict()

    def add_subscribe(self, client, topic):
        exist_subscription = self.__subscrption_list.get(client, None)
        if exist_subscription is not None:
            if topic not in exist_subscription:
                exist_subscription.append(topic)
        else:
            self.__subscrption_list[client] = [topic]

    def del_client(self, client):
        self.__subscrption_list.pop(client, None)

    def del_subscribe(self, client, topic):
        exist_subscription = self.__subscrption_list.get(client, None)
        if exist_subscription is not None:
            if topic in exist_subscription:
                exist_subscription.remove(topic)
                if len(exist_subscription) == 0:
                    self.del_client(client)

    def get_client_f_topic(self, topic):
        for client_l, topic_l in self.__subscrption_list.items():
            if topic in topic_l:
                yield client_l

    def get_topic_f_client(self, client):
        if client in self.__subscrption_list.keys():
            return self.__subscrption_list[client]

    def get_size(self):
        return len(self.__subscrption_list)


SUBSCRPTION_SESSION = Session()
