import alert
import server
import stock
import threading

if __name__ == "__main__":
    am = alert.AlertManager()

    alertThread = threading.Thread(target=am.run)
    stockThread = threading.Thread(target=stock.run,
                                   kwargs=dict(alert_manager=am))
    serverThread = threading.Thread(target=server.run,
                                    kwargs=dict(alert_manager=am))

    alertThread.start()
    stockThread.start()
    serverThread.start()

    alertThread.join()
    stockThread.join()
    serverThread.join()
