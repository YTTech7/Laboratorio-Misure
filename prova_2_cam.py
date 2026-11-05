"""Tracking di due camere con un'unica pipeline e interfaccia MATLAB stabile."""

import cv2
import mediapipe as mp

from calcola_angoli_mano import calcola_angoli_mano

# Modificare gli indici qui; apertura e riapertura usano la stessa configurazione.
CAMERA_INDICES = (1, 2)
FRAME_SIZE = (1920, 1080)
HANDS_OPTIONS = dict(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles


class CameraTracker:
    """Risorse e stato temporale indipendenti per una singola camera."""

    def __init__(self, index, window_name):
        self.index = index
        self.window_name = window_name
        self.capture = None
        self.hands = None
        self.window_open = False
        self.landmark_style = None
        self.connection_style = None

    def open(self):
        if self.capture is not None:
            return self.capture.isOpened()
        try:
            self.capture = cv2.VideoCapture(self.index)
            if not self.capture.isOpened():
                self.close()
                return False
            width, height = FRAME_SIZE
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.hands = mp_hands.Hands(**HANDS_OPTIONS)
            self.landmark_style = mp_styles.get_default_hand_landmarks_style()
            self.connection_style = mp_styles.get_default_hand_connections_style()
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            self.window_open = True
            cv2.resizeWindow(self.window_name, width, height)
            return True
        except Exception:
            self.close()
            raise

    def process(self, frame):
        """Restituisce frame BGR annotato, bounding box e angoli Left/Right."""
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        result = self.hands.process(rgb)
        boxes = []
        angles = {"Left": None, "Right": None}
        height, width = frame.shape[:2]

        for landmarks, handedness in zip(
            result.multi_hand_landmarks or [], result.multi_handedness or []
        ):
            side = handedness.classification[0].label
            xs = [lm.x for lm in landmarks.landmark]
            ys = [lm.y for lm in landmarks.landmark]
            xmin = max(0, min(width - 1, int(min(xs) * width)))
            xmax = max(0, min(width - 1, int(max(xs) * width)))
            ymin = max(0, min(height - 1, int(min(ys) * height)))
            ymax = max(0, min(height - 1, int(max(ys) * height)))
            boxes.append([xmin, ymin, xmax, ymax])
            angles[side] = calcola_angoli_mano(landmarks)
            mp_drawing.draw_landmarks(
                frame, landmarks, mp_hands.HAND_CONNECTIONS,
                self.landmark_style, self.connection_style,
            )
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(
                frame, side, (xmin, max(0, ymin - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
            )
        return frame, boxes, angles

    def close(self):
        # Azzerare prima i riferimenti rende sicure chiamate ripetute.
        capture, self.capture = self.capture, None
        hands, self.hands = self.hands, None
        window_open, self.window_open = self.window_open, False
        try:
            if capture is not None:
                capture.release()
        finally:
            try:
                if hands is not None:
                    hands.close()
            finally:
                if window_open:
                    try:
                        cv2.destroyWindow(self.window_name)
                    except cv2.error:
                        pass  # La finestra potrebbe essere stata chiusa manualmente.


# Nessuna camera, finestra o modello viene aperto durante l'importazione.
_cameras = tuple(
    CameraTracker(index, f"Camera {number}")
    for number, index in enumerate(CAMERA_INDICES, start=1)
)
last_frame_cam1 = None
last_frame_cam2 = None
_NO_FRAME = (None, None, None, None)


def get_frame_and_bbox():
    """Restituisce (bbox1, angoli1, bbox2, angoli2), oppure quattro None.

    Gli ultimi frame annotati rimangono disponibili in RGB per MATLAB.
    Dopo close_camera(), la chiamata successiva riapre entrambe le camere.
    """
    global last_frame_cam1, last_frame_cam2
    try:
        for camera in _cameras:
            if not camera.open():
                close_camera()
                return _NO_FRAME

        # Acquisire entrambi i frame prima dell'inferenza.
        frames = []
        for camera in _cameras:
            ok, frame = camera.capture.read()
            if not ok or frame is None:
                close_camera()
                return _NO_FRAME
            frames.append(frame)

        output = []
        rgb_frames = []
        for camera, frame in zip(_cameras, frames):
            annotated, boxes, angles = camera.process(frame)
            output.extend((boxes, angles))
            rgb_frames.append(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
            cv2.imshow(camera.window_name, annotated)

        last_frame_cam1, last_frame_cam2 = rgb_frames
        if cv2.waitKey(1) & 0xFF == ord("c"):
            close_camera()
            return _NO_FRAME
        return tuple(output)
    except Exception:
        close_camera()
        raise


def close_camera():
    """Rilascia camere, tracker e finestre; sicura anche prima dell'apertura."""
    global last_frame_cam1, last_frame_cam2
    last_frame_cam1 = last_frame_cam2 = None
    try:
        _cameras[0].close()
    finally:
        _cameras[1].close()
