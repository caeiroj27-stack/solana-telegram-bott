
import os
import requests
from datetime import datetime

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def main():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()["solana"]
    preco = data["usd"]
    change = data.get("usd_24h_change", 0)

    emoji = "🟢" if change >= 0 else "🔴"
    sinal = "+" if change >= 0 else ""

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    mensagem = (
        f"<b>◎ Solana – Monitoramento</b>\n\n"
        f"💰 Preço: <b>${preco:,.2f}</b>\n"
        f"📈 24h: {emoji} {sinal}{change:.2f}%\n"
        f"🕐 {agora}"
    )

    telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    r = requests.post(
        telegram,
        json={"chat_id": CHAT_ID, "text": mensagem,
              "parse_mode": "HTML"},
        timeout=20
    )
    r.raise_for_status()

    print("Mensagem enviada com sucesso!")

if __name__ == "__main__":
    main()
