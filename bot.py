import os
from datetime import datetime, timezone

import requests


def main():
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["CHAT_ID"]

    # Obter preço e variação da Solana
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": "solana",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()["solana"]

    preco = data["usd"]
    variacao = data.get("usd_24h_change", 0)
    emoji = "🟢" if variacao >= 0 else "🔴"
    sinal = "+" if variacao >= 0 else ""
    agora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    mensagem = (
        "<b>◎ Solana — Monitorização</b>\n\n"
        f"💰 Preço: <b>${preco:,.2f}</b>\n"
        f"📈 Variação 24h: {emoji} {sinal}{variacao:.2f}%\n"
        f"🕐 {agora}"
    )

    # Enviar mensagem ao Telegram
    telegram_response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": mensagem,
            "parse_mode": "HTML",
        },
        timeout=20,
    )
    telegram_response.raise_for_status()
    print("Mensagem enviada com sucesso!")


if __name__ == "__main__":
    main()
