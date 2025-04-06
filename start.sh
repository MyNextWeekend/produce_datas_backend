#!/usr/bin/env bash

APP_NAME="uvicorn"
APP_MODULE="app.main:app"
PID_FILE="fastapi_app.pid"

start() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "$APP_NAME is already running."
    else
        echo "Starting $APP_NAME..."
        nohup $APP_NAME $APP_MODULE > /dev/null 2>&1 &
        echo $! > "$PID_FILE"
        echo "$APP_NAME started."
    fi
}

stop() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Stopping $APP_NAME..."
        kill -9 $(cat "$PID_FILE") && rm -f "$PID_FILE"
        echo "$APP_NAME stopped."
    else
        echo "$APP_NAME is not running."
    fi
}

restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac