
import os
import time
import requests
from datetime import datetime

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def obter_preco():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    for tentativa in range(4):
        response = requests.get(url, params=params, timeout=20)

        if response.status_code == 429:
            espera = 20 * (2 ** tentativa)

            try:
                espera = max(espera, int(response.headers.get("Retry-After", 0)))
            except (ValueError, TypeError):
                pass

            print(f"CoinGecko limitou os pedidos. Nova tentativa em {espera}s.")
            time.sleep(espera)
            continue

        response.raise_for_status()
        return response.json()["solana"]

    raise Exception("CoinGecko continua a limitar os pedidos após 4 tentativas.")

def main():
    data = obter_preco()

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
        json={
            "chat_id": CHAT_ID,
            "text": mensagem,
            "parse_mode": "HTML"
        },
        timeout=20
    )

    r.raise_for_status()
    print("Mensagem enviada com sucesso!")

if __name__ == "__main__":
    main()
