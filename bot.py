import os
from datetime import datetime, timezone

import requests


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"A secret {name} não está configurada no GitHub Actions.")
    return value


def main():
    token = required_env("TELEGRAM_TOKEN")
    chat_id = required_env("CHAT_ID")

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

    result = telegram_response.json()
    if not result.get("ok"):
        raise RuntimeError(
            f"O Telegram recusou a mensagem: {result.get('description', 'erro desconhecido')}"
        )

    print(f"Mensagem enviada com sucesso para o chat {chat_id} às {agora}.")


if __name__ == "__main__":
    main()
