import ast
import json
import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, AWSIoTMQTTShadowClient
from proxy.utils import read_yaml_config, singleton

_PROXY = None


def aws_agt_set_proxy(proxy):
    global _PROXY
    _PROXY = proxy


def shadow_cb_update(payload, resp_stu, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print("rcv update", payload, resp_stu, token)


def shadow_cb_delta(payload, resp_stu, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print("rcv delta", payload, resp_stu, token)
    dict_payload = ast.literal_eval(payload)
    state = dict_payload.get("state", None)
    if state is not None:
        if _PROXY is not None:
            _PROXY.msg_2_nodemcu(state)


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

        self.__aws_iot_mqtt_cli.connect()

        self.__aws_iot_shadow_cli = AWSIoTMQTTShadowClient("entry_dev")
        self.__aws_iot_shadow_cli.configureEndpoint(access_point["host"], 8883)
        self.__aws_iot_shadow_cli.configureCredentials(access_point["ca_path"],
                                                       access_point["privateKey_path"],
                                                       access_point["certificate_path"])
        self.__aws_iot_shadow_cli.configureAutoReconnectBackoffTime(1, 32, 20)
        self.__aws_iot_shadow_cli.configureConnectDisconnectTimeout(10)  # 10 sec
        self.__aws_iot_shadow_cli.configureMQTTOperationTimeout(5)  # 5 sec

        self.__aws_iot_shadow_cli.connect()
        self.__device_shadow = self.__aws_iot_shadow_cli.createShadowHandlerWithName(config["thing_name"], True)
        self.__device_shadow.shadowRegisterDeltaCallback(shadow_cb_delta)

    def publish(self, data):
        for (topic, payload) in data.items():
            value = str("\"" + payload + "\"")
            self.__aws_iot_mqtt_cli.publish(topic, value, 0)
            print("send publish", topic, payload)

#    def subscribe(self, topic):
#        self.__aws_iot_mqtt_cli.subscribe(topic, 1, notify_cb)

    def update_dev_shadow(self, shadow_file):
        dict_shadow_file = dict()
        dict_shadow_file["state"] = {"reported": shadow_file, "desired": None}
        json_file = json.dumps(dict_shadow_file)
        self.__device_shadow.shadowUpdate(json_file, shadow_cb_update, 5)
        print("update shadow ", json_file)

#    def unsubscribe(self, topic):
#        self.__aws_iot_mqtt_cli.unsubscribe(topic)


if __name__ == '__main__':
    aws_iot_agt = AwsIotAgent()

    aws_iot_agt.subscribe("entry_token")
    time.sleep(2)

    loopCount = 0
    while True:
        aws_iot_agt.publish("entry_token", "New Message " + str(loopCount))
        loopCount += 1
        time.sleep(1)
