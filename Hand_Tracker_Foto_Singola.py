# ============================================================
# IMPORTAZIONE LIBRERIE
# ============================================================
#
# OpenCV:
# gestione immagini, disegno grafico e visualizzazione.
#
# MediaPipe:
# rilevamento dei landmark della mano.
#
# calcola_angoli_mano:
# funzione sviluppata per il calcolo degli angoli
# articolari a partire dai 21 landmark MediaPipe.
import cv2
import mediapipe as mp
from calcola_angoli_mano import calcola_angoli_mano
# ============================================================
# INIZIALIZZAZIONE MEDIAPIPE
# ============================================================
#
# Viene creato un oggetto Hands specifico per
# l'elaborazione di immagini statiche.
#
# static_image_mode=True:
# ogni fotografia viene elaborata in maniera indipendente.
#
# max_num_hands:massimo numero di mani ricercabili.
#
# min_detection_confidence: soglia minima di affidabilità del rilevamento.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.6
)
# ============================================================
# OGGETTI PER IL DISEGNO DEI LANDMARK
# ============================================================
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
# ============================================================
# FUNZIONE PRINCIPALE DI ELABORAZIONE
# ============================================================
#
# Input:
# percorso_immagine
# percorso completo della fotografia.
#
# Output:
# bbox_list -> lista delle bounding box individuate.
#
# angoli -> dizionario contenente gli angoli articolari delle mani rilevate.
def process_image(percorso_immagine):
    # --------------------------------------------------------
    # LETTURA IMMAGINE
    # --------------------------------------------------------
    #
    # Apertura del file immagine tramite OpenCV.
    frame = cv2.imread(percorso_immagine)
    # --------------------------------------------------------
    # CONTROLLO LETTURA
    # --------------------------------------------------------
    #
    # Se l'immagine non viene trovata o non può
    # essere aperta, la funzione termina.
    if frame is None:
        return None, None
    # --------------------------------------------------------
    # EFFETTO SPECCHIO
    # --------------------------------------------------------
    # per avere la giusta classificazione right o left
    frame = cv2.flip(frame, 1)
    # --------------------------------------------------------
    # CONVERSIONE RGB
    # --------------------------------------------------------
    #
    # MediaPipe richiede immagini RGB.
    #
    # OpenCV utilizza invece il formato BGR.
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # --------------------------------------------------------
    # ELABORAZIONE MEDIAPIPE
    # --------------------------------------------------------
    #
    # Analisi dell'immagine e ricerca delle mani.
    result = hands.process(rgb)
    # --------------------------------------------------------
    # VARIABILI DI USCITA
    # --------------------------------------------------------
    #
    # bbox_list: conterrà tutte le bounding box rilevate.
    #
    # angoli: dizionario finale contenente gli angoli articolari delle mani.
    bbox_list = []
    angoli = {
        "Left": None,
        "Right": None
    }
    # --------------------------------------------------------
    # RICERCA MANI
    # --------------------------------------------------------
    #
    # Se almeno una mano viene individuata,
    # viene eseguito un ciclo di elaborazione
    # per ogni mano rilevata.
    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(
            result.multi_hand_landmarks,
            result.multi_handedness
        ):
            # ------------------------------------------------
            # IDENTIFICAZIONE DELLA MANO
            # ------------------------------------------------
            #
            # MediaPipe classifica automaticamente
            # la mano come:
            #
            # Left
            # Right
            lato = handedness.classification[0].label
            # ------------------------------------------------
            # ESTRAZIONE COORDINATE X, Y LANDMARK PER I BOUNDING BOX
            # ------------------------------------------------
            #
            # Recupero coordinate normalizzate
            # di tutti i 21 landmark.
            xs = [lm.x for lm in hand_landmarks.landmark]
            ys = [lm.y for lm in hand_landmarks.landmark]
            # ------------------------------------------------
            # CALCOLO BOUNDING BOX
            # ------------------------------------------------
            #
            # Conversione da coordinate normalizzate
            # a coordinate pixel.
            xmin = int(min(xs) * frame.shape[1])
            xmax = int(max(xs) * frame.shape[1])
            ymin = int(min(ys) * frame.shape[0])
            ymax = int(max(ys) * frame.shape[0])
            bbox = [xmin,ymin,xmax,ymax]
            bbox_list.append(bbox)
            # ------------------------------------------------
            # CALCOLO DEGLI ANGOLI ARTICOLARI
            # ------------------------------------------------
            #
            # I 21 landmark vengono passati alla
            # funzione dedicata che restituisce:
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
            #
            # Gli angoli vengono salvati nel dizionario
            # finale utilizzando come chiave:
            #
            # Left
            # Right
            angoli[lato] = angoli_mano
            # ------------------------------------------------
            # COSTRUZIONE TABELLA TESTUALE
            # ------------------------------------------------
            #
            # Creazione delle righe che verranno
            # visualizzate sull'immagine.
            righe = [
                lato,
                f"THUMB, (CMC, MCP,  IP): {angoli_mano['THUMB_CMC']:.2f} {angoli_mano['THUMB_MCP']:.2f} {angoli_mano['THUMB_IP']:.2f}",
                f"INDEX, (MCP, PIP, DIP):{angoli_mano['INDEX_MCP']:.2f} {angoli_mano['INDEX_PIP']:.2f} {angoli_mano['INDEX_DIP']:.2f}",
                f"MIDDLE,(MCP, PIP, DIP): {angoli_mano['MIDDLE_MCP']:.2f} {angoli_mano['MIDDLE_PIP']:.2f} {angoli_mano['MIDDLE_DIP']:.2f}",
                f"RING,  (MCP, PIP, DIP):{angoli_mano['RING_MCP']:.2f} {angoli_mano['RING_PIP']:.2f} {angoli_mano['RING_DIP']:.2f}",
                f"PINKY, (MCP, PIP, DIP):{angoli_mano['PINKY_MCP']:.2f} {angoli_mano['PINKY_PIP']:.2f} {angoli_mano['PINKY_DIP']:.2f}"
            ]
            # ------------------------------------------------
            # TABELLA SOPRA AL BOUNDING BOX
            # ------------------------------------------------
            tab_w = 350
            tab_h = 130
            # allineamento al bordo sinistro della bounding box
            x_tab = xmin
            # tabella sopra la mano
            y_tab = ymin - tab_h - 10
            # se non c'è spazio sopra la mano
            # la posiziona immediatamente sotto
            if y_tab < 10:
                y_tab = ymax + 10
            # evita uscita dal bordo destro
            if x_tab + tab_w > frame.shape[1]:
                x_tab = frame.shape[1] - tab_w - 10
            # evita uscita dal bordo sinistro
            x_tab = max(10, x_tab)
            # ------------------------------------------------
            # SFONDO DELLA TABELLA
            # ------------------------------------------------
            #
            # Rettangolo nero che migliora
            # la leggibilità del testo.
            cv2.rectangle(
                frame,
                (x_tab - 10, y_tab - 20),
                (x_tab + tab_w, y_tab + tab_h),
                (0, 0, 0),
                -1
            )
            # ------------------------------------------------
            # SCRITTURA DELLE RIGHE
            # ------------------------------------------------
            for i, riga in enumerate(righe):
                cv2.putText(
                    frame,
                    riga,
                    (x_tab, y_tab + i * 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.55,
                    (0, 255, 255),
                    1,
                    cv2.LINE_AA
                )
            # ------------------------------------------------
            # DISEGNO DELLO SCHELETRO
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
            # ETICHETTA DELLA MANO
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
    # VISUALIZZAZIONE RISULTATO
    # --------------------------------------------------------
    #
    # Mostra la fotografia elaborata con:
    #
    # - scheletro MediaPipe
    # - bounding box
    # - identificazione Left / Right
    # - tabella degli angoli
    cv2.imshow("Foto elaborata", frame)
    # Attesa pressione di un tasto.
    cv2.waitKey(0)
    # Chiusura finestra OpenCV.
    cv2.destroyAllWindows()
    # --------------------------------------------------------
    # RESTITUZIONE RISULTATI
    # --------------------------------------------------------
    #
    # bbox_list:
    # lista delle bounding box.
    #
    # angoli:
    # dizionario degli angoli articolari.
    return bbox_list, angoli