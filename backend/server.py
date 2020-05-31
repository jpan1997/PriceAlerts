import alert
import eventlet
import json
import socketio
from twilio.rest import Client
import threading
import time
import requests
import websocket


def run(alert_manager):
    print("server thread running")
    sio = socketio.Server()
    app = socketio.WSGIApp(sio, static_files={'/': '../frontend/index.html'})

    # client socket event handlers
    @sio.on('connect')
    def connect(sid, environ):
        print('connect', sid)

    @sio.on('disconnect')
    def disconnect(sid):
        print('disconnect', sid)

    @sio.on('add_alert')
    def add_alert(sid, data):
        print('add_alert', data)
        alert_manager.add_alert(
            alert.Alert(data['ticker'], alert.AlertType(data['alert_type']),
                        float(data['target'])))

    @sio.on('remove_alert')
    def remove_alert(sid, data):
        print('remove_alert', data)
        alert_manager.remove_alert(
            alert.Alert(data['ticker'], alert.AlertType(data['alert_type']),
                        float(data['target'])))

    @sio.on('update_req')
    def handle_update(sid, data):
        #  print('update_req', data)

        # TODO: Fix this json hack
        alerts_json = {}
        for ticker, alerts in alert_manager.alerts.items():
            ticker_alerts_json = []
            for alert in alerts:
                ticker_alerts_json.append(alert.to_dict())
            alerts_json[ticker] = ticker_alerts_json

        sio.emit('update_resp', {
            'prices': alert_manager.prices,
            'alerts': alerts_json
        })

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)