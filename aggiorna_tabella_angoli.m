% ==========================================================
% FUNZIONE DI AGGIORNAMENTO DELLA TABELLA
% ==========================================================
%
% Input:
% tabella-> handle della tabella MATLAB da aggiornare
% angoli_mano-> dizionario Python contenente i valori degli angoli
%
% Se una mano non viene rilevata, la tabella viene
% riempita con valori NaN.
function aggiorna_tabella_angoli(tabella, angoli_mano)
    try
        tabella.Data = [

            double(angoli_mano{'THUMB_CMC'});
            double(angoli_mano{'THUMB_MCP'});
            double(angoli_mano{'THUMB_IP'});

            double(angoli_mano{'INDEX_MCP'});
            double(angoli_mano{'INDEX_PIP'});
            double(angoli_mano{'INDEX_DIP'});

            double(angoli_mano{'MIDDLE_MCP'});
            double(angoli_mano{'MIDDLE_PIP'});
            double(angoli_mano{'MIDDLE_DIP'});

            double(angoli_mano{'RING_MCP'});
            double(angoli_mano{'RING_PIP'});
            double(angoli_mano{'RING_DIP'});

            double(angoli_mano{'PINKY_MCP'});
            double(angoli_mano{'PINKY_PIP'});
            double(angoli_mano{'PINKY_DIP'})

        ];
    catch
        % Se la mano non è presente
        % vengono mostrati valori non disponibili.
        tabella.Data = NaN(15,1);
    end
end