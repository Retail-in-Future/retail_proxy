import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from proxy.nodemcu_agt import nodemcu_agt_set_proxy, NodemcuAgent
from proxy.utils import read_yaml_config, singleton

_PROXY = None


def aws_agt_set_proxy(proxy):
    global _PROXY
    _PROXY = proxy


def notify_cb(client, userdata, message):
    print(message.topic, message.payload)
    if _PROXY is not None:
        _PROXY.msg_2_nodemcu(message.topic, message.payload)


class AwsIotAgent(metaclass=singleton):
    def __init__(self):
        config = read_yaml_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'))

        access_point = {}
        if config["access_point"] == "us-east-2":
            access_point.update(config["aws_IoT_broker"]["us-east-2"])
        else:
            access_point.update(config["aws_IoT_broker"]["ap-northeast-1"])

        self.__aws_iot_mqtt_cli = AWSIoTMQTTClient("entry_point")
        self.__aws_iot_mqtt_cli.configureEndpoint(access_point["host"], 8883)
        self.__aws_iot_mqtt_cli.configureCredentials(access_point["ca_path"],
                                                     access_point["privateKey_path"], access_point["certificate_path"])

        self.__aws_iot_mqtt_cli.configureAutoReconnectBackoffTime(1, 32, 20)
        self.__aws_iot_mqtt_cli.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.__aws_iot_mqtt_cli.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.__aws_iot_mqtt_cli.configureConnectDisconnectTimeout(10)  # 10 sec
        self.__aws_iot_mqtt_cli.configureMQTTOperationTimeout(5)  # 5 sec

    def start(self):
        self.__aws_iot_mqtt_cli.connect()

    def publish(self, topic, payload):
        self.__aws_iot_mqtt_cli.publish(topic, payload, 0)

    def subscribe(self, topic):
        self.__aws_iot_mqtt_cli.subscribe(topic, 1, notify_cb)

    def unsubscribe(self, topic):
        self.__aws_iot_mqtt_cli.unsubscribe(topic)


if __name__ == '__main__':
    aws_iot_agt = AwsIotAgent()
    aws_iot_agt.start()

    aws_iot_agt.subscribe("entry_token")
    time.sleep(2)

    loopCount = 0
    while True:
        aws_iot_agt.publish("entry_token", "New Message " + str(loopCount))
        loopCount += 1
        time.sleep(1)
