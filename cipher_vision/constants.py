from os.path import join, dirname

MQTT_CLIENT_ID='vision'
MQTT_BROKER_URL='localhost'
MQTT_BROKER_PORT=1883 # default is 1883

LOG_FILE=join(dirname(__file__), 'app.log')

YOLO_WEIGHTS_PATH = join(dirname(__file__), 'yolov3.weights')
YOLO_CLASSES_PATH = join(dirname(__file__), 'yolov3.classes')
YOLO_CONFIG_PATH = join(dirname(__file__), 'yolov3.cfg')

CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
CAMERA_FRAME_RATE = 30