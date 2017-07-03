from nose.tools import ok_
from proxy.session import SUBSCRPTION_SESSION


def test_add_subscription():
    ok_(0 == SUBSCRPTION_SESSION.get_size())

    SUBSCRPTION_SESSION.add_subscribe("topic1", "val1")
    ok_(1 == SUBSCRPTION_SESSION.get_size())
    ok_(["val1"] == SUBSCRPTION_SESSION.get_topic_f_client("topic1"))

    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.1")
    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.2")
    ok_(2 == SUBSCRPTION_SESSION.get_size())
    h = SUBSCRPTION_SESSION.get_topic_f_client("topic2")
    ok_(["val2.1", "val2.2"] == SUBSCRPTION_SESSION.get_topic_f_client("topic2"))

    SUBSCRPTION_SESSION.add_subscribe("topic1", "val1.1")
    ok_(2 == SUBSCRPTION_SESSION.get_size())
    ok_(["val1", "val1.1"] == SUBSCRPTION_SESSION.get_topic_f_client("topic1"))

    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.1")
    ok_(2 == SUBSCRPTION_SESSION.get_size())
    ok_(["val2.1", "val2.2"] == SUBSCRPTION_SESSION.get_topic_f_client("topic2"))


def test_del_client():
    SUBSCRPTION_SESSION.del_client("topic1")
    ok_(1 == SUBSCRPTION_SESSION.get_size())
    SUBSCRPTION_SESSION.del_client("topic2")
    ok_(0 == SUBSCRPTION_SESSION.get_size())
    SUBSCRPTION_SESSION.del_client("topic2")
    ok_(0 == SUBSCRPTION_SESSION.get_size())


def test_del_subscription():
    SUBSCRPTION_SESSION.add_subscribe("topic1", "val1")
    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.1")
    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.2")

    SUBSCRPTION_SESSION.del_subscribe("topic3", "val3")
    ok_(2 == SUBSCRPTION_SESSION.get_size())

    SUBSCRPTION_SESSION.del_subscribe("topic1", "val1.1")
    ok_(2 == SUBSCRPTION_SESSION.get_size())
    ok_(["val1"] == SUBSCRPTION_SESSION.get_topic_f_client("topic1"))

    SUBSCRPTION_SESSION.del_subscribe("topic2", "val2.1")
    ok_(2 == SUBSCRPTION_SESSION.get_size())
    ok_(["val2.2"] == SUBSCRPTION_SESSION.get_topic_f_client("topic2"))

    SUBSCRPTION_SESSION.del_subscribe("topic2", "val2.2")
    ok_(1 == SUBSCRPTION_SESSION.get_size())

    SUBSCRPTION_SESSION.del_subscribe("topic1", "val1")
    ok_(0 == SUBSCRPTION_SESSION.get_size())


def test_get_client_f_topic():
    SUBSCRPTION_SESSION.add_subscribe("topic1", "val1")
    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.1")
    SUBSCRPTION_SESSION.add_subscribe("topic2", "val2.2")
    SUBSCRPTION_SESSION.add_subscribe("topic3", "val1")
    SUBSCRPTION_SESSION.add_subscribe("topic4", "val2.2")

    client_l1 = list()

    for client in SUBSCRPTION_SESSION.get_client_f_topic("val1"):
        client_l1.append(client)

    ok_(client_l1 == ["topic1", "topic3"])

    client_l2 = list()

    for client in SUBSCRPTION_SESSION.get_client_f_topic("val2.2"):
        client_l2.append(client)

    ok_(client_l2 == ["topic2", "topic4"])

    client_l3 = list()

    for client in SUBSCRPTION_SESSION.get_client_f_topic("val2.1"):
        client_l3.append(client)

    ok_(client_l3 == ["topic2"])

    SUBSCRPTION_SESSION.del_client("topic1")
    SUBSCRPTION_SESSION.del_client("topic2")
    SUBSCRPTION_SESSION.del_client("topic3")
    SUBSCRPTION_SESSION.del_client("topic4")
    ok_(0 == SUBSCRPTION_SESSION.get_size())

