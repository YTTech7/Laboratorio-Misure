# ============================================================
# IMPORTAZIONE DELLE LIBRERIE
# ============================================================
#
# cv2:
# libreria OpenCV utilizzata per:
# - acquisizione webcam
# - elaborazione immagini
# - visualizzazione finestre
# - disegno di testi e figure
# - prova GITHUB
#
# mediapipe:
# libreria Google per il tracciamento delle mani.
#
# calcola_angoli_mano:
# funzione sviluppata separatamente che calcola
# gli angoli articolari a partire dai landmark
# forniti da MediaPipe.
import cv2
import mediapipe as mp
from calcola_angoli_mano import calcola_angoli_mano

# ============================================================
# INIZIALIZZAZIONE MEDIAPIPE HANDS
# ============================================================
#
# Creazione dell'oggetto Hands utilizzato per il
# rilevamento e tracciamento delle mani.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(

    # Modalità video.
    # Il tracking viene mantenuto tra frame consecutivi.
    static_image_mode = False,
    # Numero massimo di mani da rilevare.
    max_num_hands = 2,
    # Soglia minima di confidenza del rilevamento.
    min_detection_confidence = 0.6,
    # Soglia minima di confidenza del tracking.
    min_tracking_confidence = 0.6
)

# ============================================================
# OGGETTI DI DISEGNO MEDIAPIPE
# ============================================================
#
# Utilizzati per visualizzare:
# - landmark
# - connessioni dello scheletro
mp_drawing = mp.solutions.drawing_utils
mp_styles   = mp.solutions.drawing_styles

# ============================================================
# INIZIALIZZAZIONE WEBCAM
# ============================================================
#
# Apertura della webcam principale.
cap = cv2.VideoCapture(0)
# Impostazione risoluzione Full HD.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# ============================================================
# ULTIMO FRAME ACQUISITO
# ============================================================
#
# Variabile globale che memorizza
# l'ultimo frame elaborato.
last_frame = None

# ============================================================
# DIZIONARIO GLOBALE DEGLI ANGOLI
# ============================================================
#
# Contiene i risultati per:
#
# Left  -> mano sinistra
# Right -> mano destra
angoli = {
    "Left": None,
    "Right": None
}

# ============================================================
# FUNZIONE PRINCIPALE
# ============================================================
#
# Restituisce:
#
# bbox_list -> lista delle bounding box rilevate.
#
# angoli -> dizionario degli angoli articolari.
def get_frame_and_bbox():
    global cap
    global last_frame
    global angoli
    # --------------------------------------------------------
    # RIAPERTURA WEBCAM
    # --------------------------------------------------------
    #
    # Se la webcam è stata precedentemente chiusa,
    # viene riaperta automaticamente.
    if cap is None:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # --------------------------------------------------------
    # ACQUISIZIONE FRAME
    # --------------------------------------------------------
    ret, frame = cap.read()
    # --------------------------------------------------------
    # CONTROLLO ACQUISIZIONE
    # --------------------------------------------------------
    #
    # Se la lettura fallisce:
    # - il frame viene annullato
    # - la funzione restituisce valori nulli
    if not ret:
        last_frame = None
        return None, None, None
    # --------------------------------------------------------
    # EFFETTO SPECCHIO
    # --------------------------------------------------------
    #
    # Ribaltamento orizzontale del frame.
    #
    # Migliora l'interazione con l'utente
    # simulando uno specchio.
    frame = cv2.flip(frame, 1)
    # --------------------------------------------------------
    # CONVERSIONE RGB
    # --------------------------------------------------------
    #
    # MediaPipe richiede immagini RGB.
    #
    # OpenCV acquisisce immagini BGR.
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # --------------------------------------------------------
    # ELABORAZIONE MEDIAPIPE
    # --------------------------------------------------------
    result = hands.process(rgb)
    # --------------------------------------------------------
    # INIZIALIZZAZIONE LISTA BOUNDING BOX
    # --------------------------------------------------------
    bbox_list = []
    # --------------------------------------------------------
    # RESET ANGOLI
    # --------------------------------------------------------
    #
    # Ad ogni frame vengono reinizializzati
    # i risultati delle mani.
    angoli = {
        "Left": None,
        "Right": None
    }
    # --------------------------------------------------------
    # RILEVAMENTO DELLE MANI
    # --------------------------------------------------------
    #
    # MediaPipe restituisce:
    #
    # result.multi_hand_landmarks -> contiene i 21 landmark di ciascuna mano rilevata.
    #
    # result.multi_handedness -> contiene la classificazione della mano (Left oppure Right).
    #
    # Se almeno una mano è stata individuata,
    # viene avviato un ciclo che analizza
    # separatamente ogni mano presente nel frame.
    if result.multi_hand_landmarks:
        # ----------------------------------------------------
        # CICLO SU TUTTE LE MANI RILEVATE
        # ----------------------------------------------------
        #
        # zip() associa ad ogni insieme di landmark
        # la relativa classificazione Left/Right.
        #
        # Ad esempio:
        #
        # Mano 1 -> landmark mano destra
        # Mano 2 -> landmark mano sinistra
        #
        # In questo modo è possibile elaborare
        # correttamente una o due mani contemporaneamente.
        for hand_landmarks, handedness in zip(
            result.multi_hand_landmarks,
            result.multi_handedness
        ):
            # ------------------------------------------------
            # IDENTIFICAZIONE MANO
            # ------------------------------------------------
            #
            # Left oppure Right.
            lato = handedness.classification[0].label
            # ------------------------------------------------
            # ESTRAZIONE COORDINATE X, Y LANDMARK PER I BOUNDING BOX
            # ------------------------------------------------
            xs = [lm.x for lm in hand_landmarks.landmark]
            ys = [lm.y for lm in hand_landmarks.landmark]
            # ------------------------------------------------
            # CALCOLO BOUNDING BOX
            # ------------------------------------------------
            xmin = int(min(xs) * frame.shape[1])
            xmax = int(max(xs) * frame.shape[1])
            ymin = int(min(ys) * frame.shape[0])
            ymax = int(max(ys) * frame.shape[0])
            bbox = [xmin, ymin, xmax, ymax]
            bbox_list.append(bbox)
            # ------------------------------------------------
            # CALCOLO ANGOLI ARTICOLARI
            # ------------------------------------------------
            #
            # La funzione utilizza i landmark (le tre coordinate)
            # di MediaPipe per determinare:
            #
            # THUMB_CMC
            # THUMB_MCP
            # THUMB_IP
            #
            # INDEX_MCP
            # INDEX_PIP
            # INDEX_DIP
            #
            # ecc.
            angoli_mano = calcola_angoli_mano(hand_landmarks)
            # ------------------------------------------------
            # MEMORIZZAZIONE RISULTATI
            # ------------------------------------------------
            angoli[lato] = angoli_mano
            # ------------------------------------------------
            # DISEGNO SCHELETRO
            # ------------------------------------------------
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )
            # ------------------------------------------------
            # DISEGNO BOUNDING BOX
            # ------------------------------------------------
            cv2.rectangle(
                frame,
                (xmin, ymin),
                (xmax, ymax),
                (0, 255, 0),
                2
            )
            # ------------------------------------------------
            # ETICHETTA LEFT / RIGHT
            # ------------------------------------------------
            cv2.putText(
                frame,
                lato,
                (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
    # --------------------------------------------------------
    # CONVERSIONE RGB DEL FRAME FINALE
    # --------------------------------------------------------
    #
    # Utilizzato per mantenere l'ultimo frame elaborato.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    last_frame = frame_rgb
    # --------------------------------------------------------
    # VISUALIZZAZIONE VIDEO
    # --------------------------------------------------------
    cv2.imshow("Hand Tracking",cv2.cvtColor(last_frame, cv2.COLOR_RGB2BGR))
    # Aggiornamento finestra OpenCV.
    cv2.waitKey(1)
    # --------------------------------------------------------
    # LETTURA TASTIERA
    # --------------------------------------------------------
    #
    # Verifica se l'utente ha premuto
    # il tasto "c" per terminare
    # l'acquisizione.
    key = cv2.waitKey(20) & 0xFF
    if key == ord('c'):
        # Chiusura webcam.
        cap.release()
        # Chiusura finestre OpenCV.
        cv2.destroyAllWindows()
        # Azzeramento handle webcam.
        cap = None
        # Segnalazione di uscita a MATLAB.
        return None, None

    # --------------------------------------------------------
    # RESTITUZIONE RISULTATI
    # --------------------------------------------------------
    #
    # bbox_list:
    # elenco delle bounding box.
    #
    # angoli:
    # dizionario contenente gli angoli
    # della mano destra e/o sinistra.
    return bbox_list, angoli