# ============================================================
# IMPORTAZIONE LIBRERIE
# ============================================================

import cv2
import mediapipe as mp
from calcola_angoli_mano import calcola_angoli_mano

# ============================================================
# MEDIAPIPE
# ============================================================
mp_hands = mp.solutions.hands
hands1 = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
hands2 = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
# ============================================================
# WEBCAM
# ============================================================
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("Camera 1", cv2.WINDOW_NORMAL)
cv2.namedWindow("Camera 2", cv2.WINDOW_NORMAL)

cv2.resizeWindow("Camera 1", 1920, 1080)
cv2.resizeWindow("Camera 2", 1920, 1080)

# ============================================================
# FRAME GLOBALI
# ============================================================

last_frame_cam1 = None
last_frame_cam2 = None

# ============================================================
# FUNZIONE PRINCIPALE
# ============================================================

def get_frame_and_bbox():

    global cap1
    global cap2

    global last_frame_cam1
    global last_frame_cam2

    # --------------------------------------------------------
    # STRUTTURE DATI CAMERA 1
    # --------------------------------------------------------

    bbox_list_cam1 = []

    angoli_cam1 = {
        "Left": None,
        "Right": None
    }

    # --------------------------------------------------------
    # STRUTTURE DATI CAMERA 2
    # --------------------------------------------------------

    bbox_list_cam2 = []

    angoli_cam2 = {
        "Left": None,
        "Right": None
    }

    # --------------------------------------------------------
    # RIAPERTURA CAMERE
    # --------------------------------------------------------

    if cap1 is None:
        cap1 = cv2.VideoCapture(1)
        cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if cap2 is None:
        cap2 = cv2.VideoCapture(0)
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # --------------------------------------------------------
    # ACQUISIZIONE FRAME
    # --------------------------------------------------------

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        return None, None, None, None

    # --------------------------------------------------------
    # SPECCHIO
    # --------------------------------------------------------

    frame1 = cv2.flip(frame1, 1)
    frame2 = cv2.flip(frame2, 1)

    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    rgb1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    # --------------------------------------------------------
    # MEDIAPIPE
    # --------------------------------------------------------

    result1 = hands1.process(rgb1)
    result2 = hands2.process(rgb2)

    # ========================================================
    # CAMERA 1
    # ========================================================

    if result1.multi_hand_landmarks:

        for hand_landmarks, handedness in zip(
            result1.multi_hand_landmarks,
            result1.multi_handedness
        ):

            lato = handedness.classification[0].label

            xs = [lm.x for lm in hand_landmarks.landmark]
            ys = [lm.y for lm in hand_landmarks.landmark]

            xmin = int(min(xs) * frame1.shape[1])
            xmax = int(max(xs) * frame1.shape[1])
            ymin = int(min(ys) * frame1.shape[0])
            ymax = int(max(ys) * frame1.shape[0])

            bbox = [xmin, ymin, xmax, ymax]
            bbox_list_cam1.append(bbox)

            angoli_cam1[lato] = calcola_angoli_mano(hand_landmarks)

            mp_drawing.draw_landmarks(
                frame1,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

            cv2.rectangle(
                frame1,
                (xmin, ymin),
                (xmax, ymax),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame1,
                lato,
                (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    # ========================================================
    # CAMERA 2
    # ========================================================

    if result2.multi_hand_landmarks:

        for hand_landmarks, handedness in zip(
            result2.multi_hand_landmarks,
            result2.multi_handedness
        ):

            lato = handedness.classification[0].label

            xs = [lm.x for lm in hand_landmarks.landmark]
            ys = [lm.y for lm in hand_landmarks.landmark]

            xmin = int(min(xs) * frame2.shape[1])
            xmax = int(max(xs) * frame2.shape[1])
            ymin = int(min(ys) * frame2.shape[0])
            ymax = int(max(ys) * frame2.shape[0])

            bbox = [xmin, ymin, xmax, ymax]
            bbox_list_cam2.append(bbox)

            angoli_cam2[lato] = calcola_angoli_mano(hand_landmarks)

            mp_drawing.draw_landmarks(
                frame2,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

            cv2.rectangle(
                frame2,
                (xmin, ymin),
                (xmax, ymax),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame2,
                lato,
                (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    # --------------------------------------------------------
    # SALVATAGGIO FRAME
    # --------------------------------------------------------

    last_frame_cam1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    last_frame_cam2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    # --------------------------------------------------------
    # VISUALIZZAZIONE
    # --------------------------------------------------------

    cv2.imshow("Camera 1", frame1)
    cv2.imshow("Camera 2", frame2)

    # --------------------------------------------------------
    # CHIUSURA
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):

        if cap1 is not None:
            cap1.release()

        if cap2 is not None:
            cap2.release()

        cv2.destroyAllWindows()

        cap1 = None
        cap2 = None

        return None, None, None, None

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    return (
        bbox_list_cam1,
        angoli_cam1,
        bbox_list_cam2,
        angoli_cam2
    )

# ============================================================
# CHIUSURA ESTERNA
# ============================================================

def close_camera():

    global cap1
    global cap2
    cap1.release()
    cap2.release()

    cap1 = None
    cap2 = None

    cv2.destroyAllWindows()