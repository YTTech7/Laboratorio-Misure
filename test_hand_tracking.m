%
% ==========================================================
% PULIZIA AMBIENTE MATLAB
% ==========================================================
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
% MATLAB deve utilizzare lo stesso interprete Python nel quale
% sono installate tutte le librerie necessarie:
%
% - MediaPipe
% - OpenCV
% - NumPy
%
% In questo caso viene utilizzato Python 3.10 installato
% nella cartella dell'utente.
pyenv("Version","C:\Users\simon\AppData\Local\Programs\Python\Python310\python.exe");
% ==========================================================
% IMPORTAZIONE DEL MODULO PYTHON
% ==========================================================
% Importa il file Hand_Tracker.py.
%
% Una volta importato, MATLAB può richiamare direttamente
% le funzioni definite nel file Python.
py.importlib.import_module('prova_2_cam');
% ==========================================================
% CREAZIONE FINESTRA MANO DESTRA
% ==========================================================
% La funzione crea:
%
% - una figura MATLAB
% - una tabella con i 15 angoli della mano
%
% La funzione restituisce:
%
% fig_dx = handle della figura
% tab_dx = handle della tabella
%             [fig_dx, tab_dx] = crea_finestra_angoli('Mano Destra');
% ==========================================================
% CREAZIONE FINESTRA MANO SINISTRA
% ==========================================================
%             [fig_sx, tab_sx] = crea_finestra_angoli('Mano Sinistra');

% ==========================================================
% AGGIORNAMENTO INIZIALE INTERFACCIA
% ==========================================================
% drawnow forza il disegno immediato delle finestre.
%
% pause(0.1) concede tempo a MATLAB per completare
% il rendering delle tabelle.
%        drawnow;
%        pause(0.1);

% ==========================================================
% CICLO PRINCIPALE
% ==========================================================
% Il ciclo viene eseguito continuamente finché:
%
% - la webcam è attiva
% - Python continua a restituire dati validi

while true
    % ------------------------------------------------------
    % ACQUISIZIONE DATI DA PYTHON
    % ------------------------------------------------------
    %
    % get_frame_and_bbox() restituisce:
    %
    % out{1} = lista bounding box
    % out{2} = dizionario degli angoli
    %
    % Gli angoli sono separati automaticamente
    % tra mano destra e mano sinistra.
    out = py.prova_2_cam.get_frame_and_bbox();

    % ------------------------------------------------------
    % CONTROLLO DI CHIUSURA
    % ------------------------------------------------------
    %
    % Quando in Python viene premuto il tasto "c"
    % la funzione restituisce:
    %
    % return None, None
    %
    % che MATLAB riceve come py.NoneType.
    %
    % In tal caso si interrompe il ciclo.
    if isa(out{1},'py.NoneType') || isa(out{2},'py.NoneType') || isa(out{3},'py.NoneType') || isa(out{4},'py.NoneType')
        break;
    end
    % ------------------------------------------------------
    % ESTRAZIONE DATI RESTITUITI DA PYTHON
    % ------------------------------------------------------
    bbox   = out{1};
    angoli = out{2};
    bbox2   = out{3};
    angoli2 = out{4};
    % ------------------------------------------------------
    % AGGIORNAMENTO TABELLA MANO DESTRA
    % ------------------------------------------------------
    %
    % Viene passato:
    %
    % - il riferimento della tabella
    % - il dizionario degli angoli della mano destra
    %           aggiorna_tabella_angoli(tab_dx,angoli{'Right'});
    % ------------------------------------------------------
    % AGGIORNAMENTO TABELLA MANO SINISTRA
    % ------------------------------------------------------
    %           aggiorna_tabella_angoli(tab_sx,angoli{'Left'});

    % ------------------------------------------------------
    % AGGIORNAMENTO GRAFICO
    % ------------------------------------------------------
    %
    % drawnow aggiorna il contenuto delle finestre.
    %
    % pause(0.01) lascia tempo al sistema operativo
    % per gestire la GUI evitando il congelamento
    % dell'interfaccia.
    %       drawnow;
    %       pause(0.01);
end



