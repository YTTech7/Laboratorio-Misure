% ==========================================================
% PULIZIA AMBIENTE MATLAB
% ==========================================================
%
% clear all :
% elimina tutte le variabili presenti nel workspace.
%
% close all :
% chiude tutte le finestre grafiche aperte.
%
% clc :
% pulisce la Command Window.
clear all; close all; clc;
% ==========================================================
% INIZIALIZZAZIONE DELL'INTERPRETE PYTHON
% ==========================================================
%
% MATLAB deve utilizzare lo stesso interprete Python nel quale
% sono installate tutte le librerie richieste:
%
% - MediaPipe
% - OpenCV
% - NumPy
%
% In questo caso viene utilizzato Python 3.10.
pyenv("Version","C:\Users\simon\AppData\Local\Programs\Python\Python310\python.exe");

% ==========================================================
% IMPORTAZIONE DEL MODULO PYTHON
% ==========================================================
%
% Importazione dello script Python dedicato
% all'elaborazione di una singola fotografia.
%
% Il file contiene la funzione:
%
% process_image(percorso_immagine)
%
% che restituisce:
%
% out{1} -> bounding box rilevate
% out{2} -> dizionario degli angoli
py.importlib.import_module('Hand_Tracker_Foto_Singola');

% ==========================================================
% CREAZIONE FINESTRA MANO DESTRA
% ==========================================================
%
% La funzione crea automaticamente:
%
% - una figura MATLAB
% - una tabella contenente i 15 angoli articolari
%
% Restituisce:
%
% fig_dx -> handle della figura
% tab_dx -> handle della tabella
[fig_dx, tab_dx] = crea_finestra_angoli('Mano Destra');
% ==========================================================
% CREAZIONE FINESTRA MANO SINISTRA
% ==========================================================
[fig_sx, tab_sx] = crea_finestra_angoli('Mano Sinistra');

% ==========================================================
% PERCORSO DELL'IMMAGINE DA ANALIZZARE
% ==========================================================
%
% Immagine contenente una o due mani.
%
% È sufficiente modificare questo percorso per
% analizzare una fotografia differente.
percorso_immagine ="C:\Users\simon\Desktop\Hand_Traker\FOTO_MANI\DX_REALE.jpg";

% ==========================================================
% ELABORAZIONE DELL'IMMAGINE
% ==========================================================
%
% Viene richiamata la funzione Python che:
%
% 1) legge la fotografia
% 2) esegue MediaPipe Hands
% 3) individua mano destra e/o sinistra
% 4) calcola tutti gli angoli articolari
% 5) restituisce bounding box e dizionario angoli
out = py.Hand_Tracker_Foto_Singola.process_image(percorso_immagine);

% ==========================================================
% ESTRAZIONE DEI RISULTATI
% ==========================================================
bbox   = out{1};
angoli = out{2};

% ==========================================================
% AGGIORNAMENTO TABELLA MANO DESTRA
% ==========================================================
%
% La funzione aggiorna automaticamente la tabella
% leggendo il dizionario Python:
%
% angoli{'Right'}
%
% Se la mano destra non viene rilevata
% vengono mostrati valori NaN.
aggiorna_tabella_angoli(tab_dx,angoli{'Right'});
% ==========================================================
% AGGIORNAMENTO TABELLA MANO SINISTRA
% ==========================================================
aggiorna_tabella_angoli(tab_sx,angoli{'Left'});

% ==========================================================
% AGGIORNAMENTO INIZIALE INTERFACCIA
% ==========================================================
% drawnow forza il disegno immediato delle finestre.
%
% pause(0.1) concede tempo a MATLAB per completare
% il rendering delle tabelle.
drawnow;

% ==========================================================
% NOTE SUGLI ANGOLI VISUALIZZATI
% ==========================================================
%
% POLLICE
%
% THUMB_CMC
% THUMB_MCP
% THUMB_IP
%
% INDICE
%
% INDEX_MCP
% INDEX_PIP
% INDEX_DIP
%
% MEDIO
%
% MIDDLE_MCP
% MIDDLE_PIP
% MIDDLE_DIP
%
% ANULARE
%
% RING_MCP
% RING_PIP
% RING_DIP
%
% MIGNOLO
%
% PINKY_MCP
% PINKY_PIP
% PINKY_DIP
%
% Tutti gli angoli sono espressi in gradi.