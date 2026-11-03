% ==========================================================
% FUNZIONE DI CREAZIONE DELLA FINESTRA DEGLI ANGOLI
% ==========================================================
%
% Input:
%
% nome -> titolo della finestra.
%
% Output:
% fig->handle della figura.
% tab-> handle della tabella associata.
function [fig,tab] = crea_finestra_angoli(nome)
    % ------------------------------------------------------
    % CREAZIONE FIGURA
    % ------------------------------------------------------
    fig = figure('Name',nome);
    % ------------------------------------------------------
    % CREAZIONE TABELLA
    % ------------------------------------------------------
    %
    % Units='normalized'
    % utilizza coordinate normalizzate tra 0 e 1.
    %
    % Position=[0 0 1 1]
    % la tabella occupa l'intera finestra.
    %
    % RowName
    % definisce il nome anatomico di ciascun angolo.
    tab = uitable( ...
        'Parent',fig,...
        'Units','normalized',...
        'Position',[0 0 1 1],...
        'Data',zeros(15,1),...
        'ColumnName',{'Angolo [deg]'},...
        'RowName',{...

        'Thumb CMC'
        'Thumb MCP'
        'Thumb IP'

        'Index MCP'
        'Index PIP'
        'Index DIP'

        'Middle MCP'
        'Middle PIP'
        'Middle DIP'

        'Ring MCP'
        'Ring PIP'
        'Ring DIP'

        'Pinky MCP'
        'Pinky PIP'
        'Pinky DIP'});
end