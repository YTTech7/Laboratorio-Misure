# ============================================================
# LIBRERIA NUMERICA
# ============================================================
#
# NumPy viene utilizzata per:
#
# - gestione vettori e matrici
# - prodotto scalare
# - norma euclidea
# - funzioni trigonometriche
#
# Tutti i calcoli geometrici degli angoli
# vengono effettuati tramite questa libreria.
import numpy as np
# ============================================================
# CALCOLO DELL'ANGOLO FRA TRE PUNTI 3D
# ============================================================
#
# Input:
# A -> primo punto
# B -> vertice dell'angolo
# C -> terzo punto
#
# Output:
# Angolo ABC espresso in gradi ->L'angolo viene calcolato utilizzando il prodotto scalare tra i vettori:
#
# BA = A - B
# BC = C - B
#
# Formula:  cos(theta) = (BA · BC) / (|BA| |BC|)
#           theta = arccos(cos(theta))
def calcola_angolo(A, B, C):
    # --------------------------------------------------------
    # COSTRUZIONE DEI VETTORI
    # --------------------------------------------------------
    #
    # BA:vettore che collega B ad A.
    #
    # BC: vettore che collega B a C.
    BA = np.array(A) - np.array(B)
    BC = np.array(C) - np.array(B)
    # --------------------------------------------------------
    # CALCOLO DELLE NORME
    # --------------------------------------------------------
    #
    # La norma rappresenta la lunghezza
    # del vettore nello spazio tridimensionale.
    norma_BA = np.linalg.norm(BA)
    norma_BC = np.linalg.norm(BC)
    # --------------------------------------------------------
    # CONTROLLO CASI DEGENERI
    # --------------------------------------------------------
    #
    # Se uno dei due vettori ha lunghezza nulla,
    # non è possibile definire l'angolo.
    #
    # Viene quindi restituito 0°.
    if norma_BA == 0 or norma_BC == 0:
        return 0.0
    # --------------------------------------------------------
    # CALCOLO DEL COSENO DELL'ANGOLO
    # --------------------------------------------------------
    cosang = np.dot(BA, BC) / (norma_BA * norma_BC)
    # --------------------------------------------------------
    # LIMITAZIONE NUMERICA
    # --------------------------------------------------------
    #
    # A causa degli errori numerici floating point,
    # il coseno potrebbe risultare leggermente
    # maggiore di 1 o minore di -1.
    #
    # Viene quindi forzato nell'intervallo
    # matematicamente valido [-1 , 1].
    cosang = np.clip(cosang, -1.0, 1.0)
    # --------------------------------------------------------
    # CALCOLO DELL'ANGOLO
    # --------------------------------------------------------
    #
    # arccos restituisce il valore in radianti.
    #
    # np.degrees converte il risultato in gradi.
    angolo = np.degrees(np.arccos(cosang))
    return angolo
# ============================================================
# CALCOLO DEGLI ANGOLI DELLA MANO
# ============================================================
#
# Input:
# hand_landmarks -> struttura dati MediaPipe contenente i 21 landmark.
#
# Output:
# dizionario Python contenente tutti gli angoli articolari della mano.
def calcola_angoli_mano(hand_landmarks):
    # --------------------------------------------------------
    # ACQUISIZIONE DEI LANDMARK
    # --------------------------------------------------------
    #
    # MediaPipe descrive una mano tramite 21 punti.
    #
    # Ogni punto possiede coordinate:
    #
    # x -> asse orizzontale
    # y -> asse verticale
    # z -> profondità
    #
    # Le coordinate vengono salvate nella lista P.
    P = []
    for lm in hand_landmarks.landmark:
        P.append([
            lm.x,
            lm.y,
            lm.z
        ])
    # --------------------------------------------------------
    # NUMERAZIONE LANDMARK MEDIAPIPE
    # --------------------------------------------------------
    #
    # 0  -> Wrist
    #
    # 1  -> Thumb CMC
    # 2  -> Thumb MCP
    # 3  -> Thumb IP
    # 4  -> Thumb Tip
    #
    # 5  -> Index MCP
    # 6  -> Index PIP
    # 7  -> Index DIP
    # 8  -> Index Tip
    #
    # 9  -> Middle MCP
    # 10 -> Middle PIP
    # 11 -> Middle DIP
    # 12 -> Middle Tip
    #
    # 13 -> Ring MCP
    # 14 -> Ring PIP
    # 15 -> Ring DIP
    # 16 -> Ring Tip
    #
    # 17 -> Pinky MCP
    # 18 -> Pinky PIP
    # 19 -> Pinky DIP
    # 20 -> Pinky Tip
    # ANGOLI:
    # --------------------------------------------------------
    # POLLICE
    # --------------------------------------------------------
    THUMB_CMC = calcola_angolo(P[0], P[1], P[2])
    THUMB_MCP = calcola_angolo(P[1], P[2], P[3])
    THUMB_IP  = calcola_angolo(P[2], P[3], P[4])
    # --------------------------------------------------------
    # INDICE
    # --------------------------------------------------------
    INDEX_MCP = calcola_angolo(P[0], P[5], P[6])
    INDEX_PIP = calcola_angolo(P[5], P[6], P[7])
    INDEX_DIP = calcola_angolo(P[6], P[7], P[8])
    # --------------------------------------------------------
    # MEDIO
    # --------------------------------------------------------
    MIDDLE_MCP = calcola_angolo(P[0], P[9], P[10])
    MIDDLE_PIP = calcola_angolo(P[9], P[10], P[11])
    MIDDLE_DIP = calcola_angolo(P[10], P[11], P[12])
    # --------------------------------------------------------
    # ANULARE
    # --------------------------------------------------------
    RING_MCP = calcola_angolo(P[0], P[13], P[14])
    RING_PIP = calcola_angolo(P[13], P[14], P[15])
    RING_DIP = calcola_angolo(P[14], P[15], P[16])
    # --------------------------------------------------------
    # MIGNOLO
    # --------------------------------------------------------
    PINKY_MCP = calcola_angolo(P[0], P[17], P[18])
    PINKY_PIP = calcola_angolo(P[17], P[18], P[19])
    PINKY_DIP = calcola_angolo(P[18], P[19], P[20])
    # --------------------------------------------------------
    # CREAZIONE DEL DIZIONARIO DEI RISULTATI
    # --------------------------------------------------------
    #
    # Tutti gli angoli vengono salvati in un
    # dizionario Python per facilitarne il passaggio
    # a MATLAB.
    angoli = {

        "THUMB_CMC": THUMB_CMC,
        "THUMB_MCP": THUMB_MCP,
        "THUMB_IP": THUMB_IP,

        "INDEX_MCP": INDEX_MCP,
        "INDEX_PIP": INDEX_PIP,
        "INDEX_DIP": INDEX_DIP,

        "MIDDLE_MCP": MIDDLE_MCP,
        "MIDDLE_PIP": MIDDLE_PIP,
        "MIDDLE_DIP": MIDDLE_DIP,

        "RING_MCP": RING_MCP,
        "RING_PIP": RING_PIP,
        "RING_DIP": RING_DIP,

        "PINKY_MCP": PINKY_MCP,
        "PINKY_PIP": PINKY_PIP,
        "PINKY_DIP": PINKY_DIP

    }
    # --------------------------------------------------------
    # RESTITUZIONE DEI RISULTATI
    # --------------------------------------------------------
    return angoli