import os
import time
import math
from typing import Dict, List

import httpx
import numpy as np
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


app = FastAPI(
    title="SEEKER BOT Signal Engine",
    version="5.1"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ASSET MAPPING
# ============================================================

FOREX = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "USD/CHF": "CHF=X",
    "NZD/USD": "NZDUSD=X",

    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "EUR/GBP": "EURGBP=X",

    "EUR/AUD": "EURAUD=X",
    "EUR/CAD": "EURCAD=X",
    "EUR/NZD": "EURNZD=X",
    "EUR/CHF": "EURCHF=X",

    "GBP/CAD": "GBPCAD=X",
    "GBP/NZD": "GBPNZD=X",
    "GBP/CHF": "GBPCHF=X",
    "GBP/AUD": "GBPAUD=X",

    "AUD/CAD": "AUDCAD=X",
    "AUD/JPY": "AUDJPY=X",
    "AUD/NZD": "AUDNZD=X",
    "AUD/CHF": "AUDCHF=X",

    "CAD/CHF": "CADCHF=X",
    "CAD/JPY": "CADJPY=X",

    "NZD/JPY": "NZDJPY=X",
    "NZD/CAD": "NZDCAD=X",
    "NZD/CHF": "NZDCHF=X",
}

CRYPTO = {
    "BTC/USD": "BTCUSDT",
    "ETH/USD": "ETHUSDT",
}

COMMODITIES = {
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "US CRUDE": "CL=F",
}


# ============================================================
# CACHE
# ============================================================

CACHE: Dict[str, dict] = {}
CACHE_SECONDS = 8


# ============================================================
# GENERAL HELPERS
# ============================================================

def clean_pair(pair: str) -> str:
    pair = str(pair).upper().strip()

    if "(OTC)" in pair:
        pair = pair.replace("(OTC)", "").strip()

    return pair


def parse_expiration(expiration: str):

    text = str(expiration).upper().strip()

    try:
        number = int(text.split()[0])
    except Exception:
        number = 1

    if "SECOND" in text:
        return number, "seconds"

    if "HOUR" in text:
        return number * 60, "minutes"

    return number, "minutes"


def choose_interval(expiration: str):

    amount, unit = parse_expiration(expiration)

    # Public reference feeds generally don't provide
    # genuine 3/5/7 second candles.
    if unit == "seconds":
        return "1m"

    if amount <= 3:
        return "1m"

    if amount <= 10:
        return "5m"

    if amount <= 30:
        return "15m"

    if amount <= 60:
        return "30m"

    return "1h"


def safe_float(value):

    try:
        value = float(value)

        if math.isfinite(value):
            return value

    except Exception:
        pass

    return None


# ============================================================
# YAHOO MARKET DATA
# ============================================================

async def fetch_yahoo(
    symbol: str,
    interval: str = "1m",
    range_value: str = "1d"
):

    url = (
        "https://query1.finance.yahoo.com"
        f"/v8/finance/chart/{symbol}"
    )

    params = {
        "interval": interval,
        "range": range_value,
        "includePrePost": "true",
        "events": "div,splits"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 SEEKER-BOT/5.1"
    }

    async with httpx.AsyncClient(
        timeout=15,
        headers=headers,
        follow_redirects=True
    ) as client:

        response = await client.get(
            url,
            params=params
        )

        response.raise_for_status()

        data = response.json()

    results = data.get("chart", {}).get("result")

    if not results:
        raise RuntimeError(
            "Yahoo Finance returned no market data."
        )

    result = results[0]

    timestamps = result.get("timestamp", [])

    indicators = result.get(
        "indicators",
        {}
    )

    quotes = indicators.get(
        "quote",
        []
    )

    if not quotes:
        raise RuntimeError(
            "Yahoo Finance returned no price candles."
        )

    quote = quotes[0]

    opens = quote.get("open", [])
    highs = quote.get("high", [])
    lows = quote.get("low", [])
    closes = quote.get("close", [])
    volumes = quote.get("volume", [])

    candles = []

    for i in range(len(timestamps)):

        try:

            o = safe_float(opens[i])
            h = safe_float(highs[i])
            l = safe_float(lows[i])
            c = safe_float(closes[i])

            if None in (o, h, l, c):
                continue

            volume = 0

            if i < len(volumes):
                volume = safe_float(
                    volumes[i]
                ) or 0

            candles.append({
                "time": timestamps[i],
                "open": o,
                "high": h,
                "low": l,
                "close": c,
                "volume": volume
            })

        except Exception:
            continue

    if len(candles) < 60:

        raise RuntimeError(
            f"Not enough market candles received "
            f"for {symbol}."
        )

    return candles


# ============================================================
# BINANCE MARKET DATA
# ============================================================

async def fetch_binance(
    symbol: str,
    interval: str = "1m"
):

    url = (
        "https://data-api.binance.vision"
        "/api/v3/klines"
    )

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 300
    }

    async with httpx.AsyncClient(
        timeout=15,
        follow_redirects=True
    ) as client:

        response = await client.get(
            url,
            params=params
        )

        response.raise_for_status()

        data = response.json()

    candles = []

    for row in data:

        try:

            candles.append({
                "time": int(row[0] / 1000),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5])
            })

        except Exception:
            continue

    if len(candles) < 60:

        raise RuntimeError(
            f"Not enough Binance candles received "
            f"for {symbol}."
        )

    return candles


# ============================================================
# EMA
# ============================================================

def ema(values, period):

    values = np.asarray(
        values,
        dtype=float
    )

    result = np.full(
        len(values),
        np.nan
    )

    if len(values) < period:
        return result

    result[period - 1] = np.mean(
        values[:period]
    )

    alpha = 2.0 / (period + 1)

    for i in range(period, len(values)):

        result[i] = (
            alpha * values[i]
            +
            (1 - alpha) * result[i - 1]
        )

    return result


# ============================================================
# SMA
# ============================================================

def sma(values, period):

    values = np.asarray(
        values,
        dtype=float
    )

    result = np.full(
        len(values),
        np.nan
    )

    if len(values) < period:
        return result

    for i in range(
        period - 1,
        len(values)
    ):

        result[i] = np.mean(
            values[
                i - period + 1:
                i + 1
            ]
        )

    return result


# ============================================================
# RSI
# ============================================================

def rsi(values, period=14):

    values = np.asarray(
        values,
        dtype=float
    )

    result = np.full(
        len(values),
        np.nan
    )

    if len(values) <= period:
        return result

    delta = np.diff(values)

    gains = np.maximum(
        delta,
        0
    )

    losses = np.maximum(
        -delta,
        0
    )

    avg_gain = np.mean(
        gains[:period]
    )

    avg_loss = np.mean(
        losses[:period]
    )

    if avg_loss == 0:
        result[period] = 100

    else:

        rs = avg_gain / avg_loss

        result[period] = (
            100 -
            (100 / (1 + rs))
        )

    for i in range(
        period + 1,
        len(values)
    ):

        gain = gains[i - 1]
        loss = losses[i - 1]

        avg_gain = (
            (
                avg_gain * (period - 1)
            ) + gain
        ) / period

        avg_loss = (
            (
                avg_loss * (period - 1)
            ) + loss
        ) / period

        if avg_loss == 0:

            result[i] = 100

        else:

            rs = avg_gain / avg_loss

            result[i] = (
                100 -
                (100 / (1 + rs))
            )

    return result


# ============================================================
# ATR
# ============================================================

def atr(
    highs,
    lows,
    closes,
    period=14
):

    highs = np.asarray(
        highs,
        dtype=float
    )

    lows = np.asarray(
        lows,
        dtype=float
    )

    closes = np.asarray(
        closes,
        dtype=float
    )

    tr = np.zeros(
        len(closes)
    )

    for i in range(
        1,
        len(closes)
    ):

        tr[i] = max(
            highs[i] - lows[i],
            abs(
                highs[i] -
                closes[i - 1]
            ),
            abs(
                lows[i] -
                closes[i - 1]
            )
        )

    result = np.full(
        len(closes),
        np.nan
    )

    if len(closes) <= period:
        return result

    result[period] = np.mean(
        tr[1:period + 1]
    )

    for i in range(
        period + 1,
        len(closes)
    ):

        result[i] = (
            (
                result[i - 1] *
                (period - 1)
            )
            +
            tr[i]
        ) / period

    return result


# ============================================================
# MACD
# ============================================================

def macd(values):

    fast = ema(
        values,
        12
    )

    slow = ema(
        values,
        26
    )

    line = fast - slow

    valid = line[
        ~np.isnan(line)
    ]

    full_signal = np.full(
        len(values),
        np.nan
    )

    if len(valid) >= 9:

        signal_values = ema(
            valid,
            9
        )

        indexes = np.where(
            ~np.isnan(line)
        )[0]

        start = indexes[0]

        for j, value in enumerate(
            signal_values
        ):

            index = start + j

            if index < len(
                full_signal
            ):

                full_signal[index] = value

    histogram = (
        line -
        full_signal
    )

    return (
        line,
        full_signal,
        histogram
    )


# ============================================================
# SIGNAL ANALYSIS
# ============================================================

def generate_analysis(
    candles: List[dict],
    expiration: str
):

    closes = np.array(
        [
            candle["close"]
            for candle in candles
        ],
        dtype=float
    )

    highs = np.array(
        [
            candle["high"]
            for candle in candles
        ],
        dtype=float
    )

    lows = np.array(
        [
            candle["low"]
            for candle in candles
        ],
        dtype=float
    )

    volumes = np.array(
        [
            candle["volume"]
            for candle in candles
        ],
        dtype=float
    )

    e9 = ema(
        closes,
        9
    )

    e21 = ema(
        closes,
        21
    )

    e50 = ema(
        closes,
        50
    )

    rsi14 = rsi(
        closes,
        14
    )

    macd_line, macd_signal, macd_hist = macd(
        closes
    )

    atr14 = atr(
        highs,
        lows,
        closes,
        14
    )

    middle = sma(
        closes,
        20
    )

    std = np.full(
        len(closes),
        np.nan
    )

    for i in range(
        19,
        len(closes)
    ):

        std[i] = np.std(
            closes[
                i - 19:
                i + 1
            ]
        )

    upper = (
        middle +
        2 * std
    )

    lower = (
        middle -
        2 * std
    )

    i = len(closes) - 1

    price = closes[i]

    score = 0

    reasons = []

    # --------------------------------------------------------
    # EMA TREND
    # --------------------------------------------------------

    if not any(
        np.isnan(
            [
                e9[i],
                e21[i],
                e50[i]
            ]
        )
    ):

        if (
            e9[i] >
            e21[i] >
            e50[i]
        ):

            score += 25

            reasons.append(
                "EMA trend is bullish."
            )

        elif (
            e9[i] <
            e21[i] <
            e50[i]
        ):

            score -= 25

            reasons.append(
                "EMA trend is bearish."
            )

        elif e9[i] > e21[i]:

            score += 10

            reasons.append(
                "Short-term EMA momentum is bullish."
            )

        elif e9[i] < e21[i]:

            score -= 10

            reasons.append(
                "Short-term EMA momentum is bearish."
            )

    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    current_rsi = rsi14[i]

    if not np.isnan(
        current_rsi
    ):

        if (
            52 <=
            current_rsi <=
            68
        ):

            score += 15

            reasons.append(
                f"RSI supports upward momentum "
                f"({current_rsi:.1f})."
            )

        elif (
            32 <=
            current_rsi <=
            48
        ):

            score -= 15

            reasons.append(
                f"RSI supports downward momentum "
                f"({current_rsi:.1f})."
            )

        elif current_rsi > 72:

            score -= 5

            reasons.append(
                f"RSI is overbought "
                f"({current_rsi:.1f})."
            )

        elif current_rsi < 28:

            score += 5

            reasons.append(
                f"RSI is oversold "
                f"({current_rsi:.1f})."
            )

    # --------------------------------------------------------
    # MACD
    # --------------------------------------------------------

    if not np.isnan(
        macd_hist[i]
    ):

        if macd_hist[i] > 0:

            score += 20

            reasons.append(
                "MACD momentum is positive."
            )

        elif macd_hist[i] < 0:

            score -= 20

            reasons.append(
                "MACD momentum is negative."
            )

    # --------------------------------------------------------
    # RECENT PRICE MOMENTUM
    # --------------------------------------------------------

    recent_returns = []

    for n in range(
        1,
        6
    ):

        if i - n >= 0:

            previous = closes[
                i - n
            ]

            current = closes[
                i - n + 1
            ]

            if previous != 0:

                recent_returns.append(
                    (
                        current -
                        previous
                    )
                    /
                    previous
                )

    momentum = sum(
        recent_returns
    )

    if momentum > 0:

        score += 10

        reasons.append(
            "Recent price momentum is positive."
        )

    elif momentum < 0:

        score -= 10

        reasons.append(
            "Recent price momentum is negative."
        )

    # --------------------------------------------------------
    # BOLLINGER BANDS
    # --------------------------------------------------------

    if not any(
        np.isnan(
            [
                upper[i],
                lower[i],
                middle[i]
            ]
        )
    ):

        band_width = (
            upper[i] -
            lower[i]
        )

        if band_width > 0:

            position = (
                price -
                lower[i]
            ) / band_width

            if position > 0.65:

                score += 5

                reasons.append(
                    "Price is in the upper Bollinger region."
                )

            elif position < 0.35:

                score -= 5

                reasons.append(
                    "Price is in the lower Bollinger region."
                )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    if len(volumes) >= 20:

        current_volume = volumes[i]

        average_volume = np.mean(
            volumes[
                i - 19:
                i
            ]
        )

        if average_volume > 0:

            if (
                current_volume >
                average_volume * 1.15
            ):

                if closes[i] > closes[i - 1]:

                    score += 5

                    reasons.append(
                        "Above-average volume confirms upward movement."
                    )

                elif closes[i] < closes[i - 1]:

                    score -= 5

                    reasons.append(
                        "Above-average volume confirms downward movement."
                    )

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    score = max(
        -100,
        min(
            100,
            int(round(score))
        )
    )

    # Directional signal when data is available.
    if score >= 0:
        signal = "BUY"
    else:
        signal = "SELL"

    # This is strength, NOT guaranteed probability.
    confidence = (
        50 +
        abs(score) * 0.45
    )

    confidence = max(
        50,
        min(
            95,
            confidence
        )
    )

    quality = "GOOD"

    if len(candles) < 100:
        quality = "LIMITED"

    if len(reasons) < 2:
        quality = "LOW"

    return {
        "signal": signal,
        "score": score,
        "confidence": round(
            confidence,
            1
        ),
        "price": round(
            float(price),
            8
        ),
        "reasons": reasons[:6],
        "data_quality": quality,
        "candle_count": len(candles),
        "timeframe": choose_interval(
            expiration
        )
    }


# ============================================================
# SYNTHETIC FOREX FALLBACK
# ============================================================

async def synthetic_forex(
    pair: str,
    interval: str
):

    synthetic_map = {

        "CAD/CHF": (
            "CAD=X",
            "CHF=X"
        ),

        "AUD/CAD": (
            "AUDUSD=X",
            "CAD=X"
        ),

        "EUR/CAD": (
            "EURUSD=X",
            "CAD=X"
        ),

        "GBP/CAD": (
            "GBPUSD=X",
            "CAD=X"
        ),

        "NZD/CAD": (
            "NZDUSD=X",
            "CAD=X"
        ),

        "EUR/CHF": (
            "EURUSD=X",
            "CHF=X"
        ),

        "GBP/CHF": (
            "GBPUSD=X",
            "CHF=X"
        ),

        "AUD/CHF": (
            "AUDUSD=X",
            "CHF=X"
        ),

        "NZD/CHF": (
            "NZDUSD=X",
            "CHF=X"
        ),

        "CAD/JPY": (
            "CAD=X",
            "JPY=X"
        ),

        "AUD/JPY": (
            "AUDUSD=X",
            "JPY=X"
        ),

        "NZD/JPY": (
            "NZDUSD=X",
            "JPY=X"
        ),

        "EUR/AUD": (
            "EURUSD=X",
            "AUDUSD=X"
        ),

        "EUR/NZD": (
            "EURUSD=X",
            "NZDUSD=X"
        ),

        "GBP/AUD": (
            "GBPUSD=X",
            "AUDUSD=X"
        ),

        "GBP/NZD": (
            "GBPUSD=X",
            "NZDUSD=X"
        ),

        "AUD/NZD": (
            "AUDUSD=X",
            "NZDUSD=X"
        )
    }

    if pair not in synthetic_map:
        return None

    first_symbol, second_symbol = (
        synthetic_map[pair]
    )

    try:

        first = await fetch_yahoo(
            first_symbol,
            interval,
            "1d"
        )

        second = await fetch_yahoo(
            second_symbol,
            interval,
            "1d"
        )

    except Exception:
        return None

    count = min(
        len(first),
        len(second)
    )

    if count < 60:
        return None

    candles = []

    for i in range(count):

        a = first[i]
        b = second[i]

        if (
            a["open"] <= 0
            or a["high"] <= 0
            or a["low"] <= 0
            or a["close"] <= 0
            or b["open"] <= 0
            or b["high"] <= 0
            or b["low"] <= 0
            or b["close"] <= 0
        ):
            continue

        candles.append({

            "time": a["time"],

            "open":
                a["open"] /
                b["open"],

            "high":
                a["high"] /
                b["high"],

            "low":
                a["low"] /
                b["low"],

            "close":
                a["close"] /
                b["close"],

            "volume": 0
        })

    return candles


# ============================================================
# GET MARKET DATA
# ============================================================

async def get_market_data(
    pair: str,
    expiration: str
):

    clean = clean_pair(
        pair
    )

    interval = choose_interval(
        expiration
    )

    # --------------------------------------------------------
    # CRYPTO
    # --------------------------------------------------------

    if clean in CRYPTO:

        symbol = CRYPTO[
            clean
        ]

        candles = await fetch_binance(
            symbol,
            interval
        )

        return (
            candles,
            "Binance public market data",
            False
        )

    # --------------------------------------------------------
    # FOREX
    # --------------------------------------------------------

    if clean in FOREX:

        symbol = FOREX[
            clean
        ]

        try:

            candles = await fetch_yahoo(
                symbol,
                interval,
                "1d"
            )

            return (
                candles,
                "Yahoo Finance reference data",
                False
            )

        except Exception:

            candles = await synthetic_forex(
                clean,
                interval
            )

            if candles:

                return (
                    candles,
                    "Yahoo Finance synthetic reference",
                    False
                )

            raise

    # --------------------------------------------------------
    # COMMODITIES
    # --------------------------------------------------------

    if clean in COMMODITIES:

        symbol = COMMODITIES[
            clean
        ]

        candles = await fetch_yahoo(
            symbol,
            interval,
            "5d"
        )

        return (
            candles,
            "Yahoo Finance reference data",
            False
        )

    raise RuntimeError(
        f"Unsupported asset: {clean}"
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():

    return {
        "ok": True,
        "service": "SEEKER BOT V5.1",
        "message": "Signal engine is running.",
        "endpoints": [
            "/api/health",
            "/api/pairs",
            "/api/signal"
        ]
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
async def health():

    return {
        "ok": True,
        "status": "online",
        "service": "SEEKER BOT Signal Engine",
        "version": "5.1",
        "timestamp": int(
            time.time()
        )
    }


# ============================================================
# PAIRS
# ============================================================

@app.get("/api/pairs")
async def pairs():

    all_pairs = []

    for name in FOREX:
        all_pairs.append(
            f"{name} (OTC)"
        )

    for name in CRYPTO:
        all_pairs.append(
            f"{name} (OTC)"
        )

    for name in COMMODITIES:
        all_pairs.append(
            f"{name} (OTC)"
        )

    return {
        "ok": True,
        "pairs": all_pairs
    }


# ============================================================
# SIGNAL API
# ============================================================

@app.get("/api/signal")
async def signal(

    pair: str = Query(...),

    expiration: str = Query(...)

):

    clean = clean_pair(
        pair
    )

    cache_key = (
        f"{clean}|{expiration}"
    )

    now = time.time()

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    cached = CACHE.get(
        cache_key
    )

    if cached:

        if (
            now -
            cached["timestamp"]
            <
            CACHE_SECONDS
        ):

            result = (
                cached["data"].copy()
            )

            result["cached"] = True

            return JSONResponse(
                status_code=200,
                content=result
            )

    # --------------------------------------------------------
    # MARKET DATA
    # --------------------------------------------------------

    try:

        (
            candles,
            source,
            broker_otc
        ) = await get_market_data(
            clean,
            expiration
        )

        analysis = generate_analysis(
            candles,
            expiration
        )

        result = {

            "ok": True,

            "signal":
                analysis["signal"],

            "action":
                analysis["signal"],

            "direction":
                analysis["signal"],

            "side":
                analysis["signal"],

            "recommendation":
                analysis["signal"],

            "pair":
                clean,

            "asset":
                clean,

            "expiration":
                expiration,

            "price":
                analysis["price"],

            "score":
                analysis["score"],

            "confidence":
                analysis["confidence"],

            "strength":
                analysis["confidence"],

            "signal_strength":
                analysis["confidence"],

            "source":
                source,

            "data_source":
                source,

            "broker_otc":
                broker_otc,

            "timeframe":
                analysis["timeframe"],

            "data_quality":
                analysis["data_quality"],

            "candle_count":
                analysis["candle_count"],

            "reasons":
                analysis["reasons"],

            "analysis":
                analysis["reasons"],

            "timestamp":
                int(time.time()),

            "cached":
                False,

            "notice":
                (
                    "This signal uses reference "
                    "market data. It is not a "
                    "guaranteed Quotex or Pocket "
                    "Option OTC quote."
                )
        }

        CACHE[cache_key] = {

            "timestamp": now,

            "data": result
        }

        return JSONResponse(
            status_code=200,
            content=result
        )

    except Exception as exc:

        error_message = str(
            exc
        )

        return JSONResponse(

            status_code=503,

            content={

                "ok": False,

                "error":
                    "MARKET_DATA_ERROR",

                "message":
                    error_message,

                "detail":
                    error_message,

                "pair":
                    clean,

                "expiration":
                    expiration,

                "signal":
                    None,

                "timestamp":
                    int(time.time())
            }
        )


# ============================================================
# LOCAL START
# ============================================================

if __name__ == "__main__":

    import uvicorn

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
