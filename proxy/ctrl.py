from proxy.aws_iot_agt import AwsIotAgent, aws_agt_set_proxy
from proxy.nodemcu_agt import NodemcuAgent, nodemcu_agt_set_proxy
from proxy.session import SUBSCRPTION_SESSION
from proxy.utils import singleton


class Proxy(metaclass=singleton):
    def __init__(self, p_aws_agt, p_nodemcu_agt):
        self.__aws_iot_agt = p_aws_agt
        self.__nodemcu_agt = p_nodemcu_agt

    def msg_2_aws(self, client, method, data):
        if "qrcode" == method:
            self.__aws_iot_agt.publish(data)
            SUBSCRPTION_SESSION.add_subscribe(client, "dev_shadow")
        elif "dev_state" == method:
            self.__aws_iot_agt.update_dev_shadow(data)
            SUBSCRPTION_SESSION.add_subscribe(client, "dev_shadow")
        elif "disconnect" == method:
            SUBSCRPTION_SESSION.del_client(client)

    def msg_2_nodemcu(self, payload):
        for client in SUBSCRPTION_SESSION.get_client_f_topic("dev_shadow"):
            self.__nodemcu_agt.send_data(client, payload)
            print("send data to nodemcu", client, payload)


if __name__ == '__main__':
    aws_iot_agt = AwsIotAgent()
    nodemcu_agt = NodemcuAgent()
    retail_proxy = Proxy(aws_iot_agt, nodemcu_agt)

    nodemcu_agt_set_proxy(retail_proxy)
    aws_agt_set_proxy(retail_proxy)

    nodemcu_agt.start()
