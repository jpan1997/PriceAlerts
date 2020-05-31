import alert


def test_alert_manager():
    am = alert.AlertManager()

    # Init state
    assert am.prices == {}
    assert am.alerts == {}

    # Add alert1
    alert1 = alert.Alert("SPY", alert.AlertType.MOVES_BELOW, 300)
    am.add_alert(alert1)
    assert am.prices == {}
    assert am.alerts == {"SPY": [alert1]}
    assert am.get_stock_list() == ["SPY"]

    # Add alert2
    alert2 = alert.Alert("SPY", alert.AlertType.MOVES_ABOVE, 300)
    am.add_alert(alert2)
    assert am.prices == {}
    assert am.alerts == {"SPY": [alert1, alert2]}

    # No price update yet
    assert not am.check_alert(alert1)
    assert am.check_all_alerts() == []

    # Update price, trigger alert2
    am.update_price("SPY", 301)
    assert am.prices == {"SPY": 301}
    assert not am.check_alert(alert1)
    assert am.check_alert(alert2)
    assert am.check_all_alerts() == [alert2]
    assert am.alert_msg(alert2) == "SPY moved above $300, price: $301"

    # Remove alert2
    am.remove_alert(alert2)
    assert am.prices == {"SPY": 301}
    assert am.alerts == {"SPY": [alert1]}
    assert am.get_stock_list() == ["SPY"]

    # Update price, trigger alert1
    am.update_price("SPY", 299)
    assert am.prices == {"SPY": 299}
    assert am.check_alert(alert1)
    assert am.check_all_alerts() == [alert1]
    assert am.alert_msg(alert1) == "SPY moved below $300, price: $299"

    # Remove alert1
    am.remove_alert(alert1)
    assert am.prices == {}
    assert am.alerts == {}
    assert am.get_stock_list() == []


def test_alert():
    alert1 = alert.Alert("SPY", alert.AlertType.MOVES_BELOW, 300)
    assert alert1.__repr__() == "(SPY, AlertType.MOVES_BELOW, 300)"

    alert2 = alert.Alert("SPY", alert.AlertType.MOVES_ABOVE, 300)
    assert alert2.__repr__() == "(SPY, AlertType.MOVES_ABOVE, 300)"

    alert3 = alert.Alert("SPY", alert.AlertType.MOVES_BELOW, 300)

    assert not alert1 == alert2
    assert alert1 == alert3


if __name__ == "__main__":
    test_alert_manager()
    test_alert()