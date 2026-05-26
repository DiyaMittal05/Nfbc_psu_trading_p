"""Route user queries to PSU, NBFC, or both universes."""

import re
from src.config.settings import PSU_TICKERS, NBFC_TICKERS, MACRO_KEYWORDS


class UniverseRouter:
    def __init__(self):
        self.psu_tickers = set(t.upper() for t in PSU_TICKERS)
        self.nbfc_tickers = set(t.upper() for t in NBFC_TICKERS)
        self.macro_keywords = [kw.lower() for kw in MACRO_KEYWORDS]

    def route(self, query: str, headline: str = "") -> dict:
        """
        Analyze query + headline and return routing decision.
        Returns: {"universes": ["psu"|"nbfc"|"both"], "tickers": [...], "macro": bool}
        """
        text = f"{query} {headline}".upper()
        text_lower = f"{query} {headline}".lower()

        found_psu = [t for t in self.psu_tickers if t in text or t.replace(".NS", "") in text]
        found_nbfc = [t for t in self.nbfc_tickers if t in text or t.replace(".NS", "").replace(".BO", "") in text]

        # Universe keyword triggers
        psu_triggers = ["psu", "public sector bank", "public sector", "government bank", "sbi", "state bank"]
        nbfc_triggers = ["nbfc", "non-banking", "finance company", "consumer finance", "gold loan", "microfinance"]

        psu_triggered = any(t in text_lower for t in psu_triggers)
        nbfc_triggered = any(t in text_lower for t in nbfc_triggers)

        # Macro keyword check
        is_macro = any(kw in text_lower for kw in self.macro_keywords)

        universes = set()
        if found_psu or psu_triggered:
            universes.add("psu")
        if found_nbfc or nbfc_triggered:
            universes.add("nbfc")

        # If both PSU and NBFC tickers explicitly mentioned, route both
        if found_psu and found_nbfc:
            universes = {"psu", "nbfc"}

        # If no universe detected but macro keywords present, route both
        if not universes and is_macro:
            universes = {"psu", "nbfc"}

        # Default fallback
        if not universes:
            universes = {"psu"}  # conservative default

        tickers = list(set(found_psu + found_nbfc))

        return {
            "universes": sorted(universes),
            "tickers": tickers,
            "macro": is_macro,
        }
