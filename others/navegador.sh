#!/bin/bash

# Função para alimentação do watchdog
watchdog_reset() {
    echo "V" > /dev/watchdog 2>/dev/null
}

# Inicia o Firefox-ESR em modo kiosk
start_firefox() {
    firefox-esr --kiosk &
}

# Refresh sem roubar o foco
refresh_page() {
    WIN_ID=$(xdotool search --onlyvisible --class "firefox" | head -n 1)
    if [ -n "$WIN_ID" ]; then
        echo "Dando refresh (sem ativar janela)..."
        DISPLAY=:0 xdotool key --window $WIN_ID "F5"
    else
        echo "Firefox não encontrado para refresh."
    fi
}

# Detecta travamento sem ativar janela
check_freeze() {
    # Se não houver janela Firefox visível, está travado
    if ! xdotool search --onlyvisible --class "firefox" >/dev/null 2>&1; then
        echo "Firefox travou, reiniciando..."
        pkill firefox-esr
        sleep 2
        start_firefox
        sleep 10
        refresh_page
    fi
}

# Teste de rede via HTTP 200
check_network() {
    curl -I --max-time 5 https://gpa.tolife.app 2>/dev/null | head -n 1 | grep "200" >/dev/null
}

# Espera a rede voltar
wait_network_restore() {
    echo "Rede caiu! Aguardando retorno de gpa.tolife.app..."

    # Aguarda o retorno da rede
    while ! check_network; do
        sleep 2
        watchdog_reset
    done

    echo "Rede voltou! Estabilizando..."
    sleep 3

    refresh_page
}

# Início do Script
start_firefox
sleep 6
refresh_page

# Loop principal
while true; do
    watchdog_reset

    # Firefox fechou?
    if ! pgrep -x "firefox-esr" >/dev/null; then
        echo "Firefox foi fechado, reiniciando..."
        start_firefox
        sleep 15
        refresh_page
    else
        check_freeze
    fi

    # Rede caiu?
    if ! check_network; then
        wait_network_restore
    fi

    sleep 10
done

