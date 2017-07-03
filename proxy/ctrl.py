from proxy.aws_iot_agt import AwsIotAgent, aws_agt_set_proxy
from proxy.nodemcu_agt import NodemcuAgent, nodemcu_agt_set_proxy
from proxy.session import SUBSCRPTION_SESSION
from proxy.utils import singleton


class Proxy(metaclass=singleton):
    def __init__(self, p_aws_agt, p_nodemcu_agt):
        self.__aws_iot_agt = p_aws_agt
        self.__nodemcu_agt = p_nodemcu_agt

    def msg_2_aws(self, client, method, data):
        if "pub" == method:
            for (topic, payload) in data.items():
                self.__aws_iot_agt.publish(topic, payload)
        elif "sub" == method:
            self.__aws_iot_agt.subscribe(data)
            SUBSCRPTION_SESSION.add_subscribe(client, data)
        elif "unsub" == method:
            self.__aws_iot_agt.unsubscribe(data)
            SUBSCRPTION_SESSION.del_subscribe(client, data)
        else:
            SUBSCRPTION_SESSION.del_client(client)

    def msg_2_nodemcu(self, topic, payload):
        for client in SUBSCRPTION_SESSION.get_client_f_topic(topic):
            self.__nodemcu_agt.send_data(client, payload)


if __name__ == '__main__':
    aws_iot_agt = AwsIotAgent()
    nodemcu_agt = NodemcuAgent()
    retail_proxy = Proxy(aws_iot_agt, nodemcu_agt)

    nodemcu_agt_set_proxy(retail_proxy)
    aws_agt_set_proxy(retail_proxy)

    aws_iot_agt.start()
    nodemcu_agt.start()
