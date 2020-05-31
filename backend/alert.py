from enum import Enum
import json
import text
import threading
# TODO: organize imports


class AlertType(Enum):
    MOVES_BELOW = "MOVES_BELOW"
    MOVES_ABOVE = "MOVES_ABOVE"

    def text(self):
        if self == AlertType.MOVES_BELOW:
            return "below"
        elif self == AlertType.MOVES_ABOVE:
            return "above"


class Alert:
    def __init__(self, ticker, alert_type, target):
        self.ticker = ticker
        self.alert_type = alert_type
        self.target = target

    def __repr__(self):
        return '({}, {}, {})'.format(self.ticker, self.alert_type, self.target)

    def __eq__(self, other):
        if not isinstance(other, Alert):
            return False
        return self.ticker == other.ticker and \
            self.alert_type == other.alert_type and \
            self.target == other.target

    # TODO; consider makign this json serializable
    # TODO: Add test
    def to_dict(self):
        return {
            "ticker": self.ticker,
            "alert_type": self.alert_type.name,
            "target": self.target
        }


class AlertManager:
    def __init__(self):
        self.prices = {}
        self.alerts = {}

    def __repr__(self):
        return 'prices: {}, alerts: {}'.format(self.prices, self.alerts)

    def get_stock_list(self):
        return list(self.alerts.keys())

    def update_price(self, ticker, price):
        if price is not None:  # TODO: add test for price = None
            self.prices[ticker] = price

    def add_alert(self, alert):
        if alert.ticker not in self.alerts:
            self.alerts[alert.ticker] = []
        self.alerts[alert.ticker].append(alert)
        print("New alert added:", alert)

    def remove_alert(self, alert):
        if alert.ticker in self.alerts:
            self.alerts[alert.ticker].remove(alert)
            if len(self.alerts[alert.ticker]) == 0:
                self.alerts.pop(alert.ticker)
                self.prices.pop(alert.ticker)
        print("Alert removed:", alert)

    def check_alert(self, alert):
        if alert.ticker in self.prices:
            if alert.alert_type == AlertType.MOVES_BELOW:
                return alert.target >= self.prices[alert.ticker]
            elif alert.alert_type == AlertType.MOVES_ABOVE:
                return alert.target <= self.prices[alert.ticker]

    def check_all_alerts(self):
        triggered_alerts = []
        for _, alerts in self.alerts.items():
            for alert in alerts:
                if self.check_alert(alert):
                    triggered_alerts.append(alert)
        return triggered_alerts

    def alert_msg(self, alert):
        return '{} moved {} ${}, price: ${}'.format(alert.ticker,
                                                    alert.alert_type.text(),
                                                    alert.target,
                                                    self.prices[alert.ticker])

    def run(self):
        print("alert thread running")
        ticker = threading.Event()
        while not ticker.wait(1):
            triggered_alerts = self.check_all_alerts()
            for alert in triggered_alerts:
                text.send_alert(self.alert_msg(alert))
                self.remove_alert(alert)