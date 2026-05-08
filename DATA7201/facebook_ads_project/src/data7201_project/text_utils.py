"""Small text and URL helpers shared by local project tooling."""

from __future__ import annotations

import re
from urllib.parse import urlsplit

URL_RE = re.compile(
    r"(?i)\b((?:https?://|www\.)[^\s<>'\"()]+|[a-z0-9.-]+\.[a-z]{2,}(?:/[^\s<>'\"()]*)?)"
)


def normalise_domain(value: str | None) -> str | None:
    """Return a lower-case registrable-looking host without a leading www."""
    if not value:
        return None

    candidate = value.strip().strip(".,;:!?)(")
    if not candidate:
        return None

    if "://" not in candidate:
        candidate = "https://" + candidate

    host = urlsplit(candidate).netloc.lower()
    if "@" in host:
        host = host.rsplit("@", 1)[-1]
    if ":" in host:
        host = host.split(":", 1)[0]
    if host.startswith("www."):
        host = host[4:]

    return host or None


def extract_domains(text: str | None) -> list[str]:
    """Extract unique domains from a text field while preserving first-seen order."""
    if not text:
        return []

    domains: list[str] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(text):
        domain = normalise_domain(match.group(1))
        if domain and domain not in seen:
            seen.add(domain)
            domains.append(domain)
    return domains


def keyword_pattern(keywords: list[str]) -> str:
    """Build a conservative case-insensitive regex for keyword/phrase matching."""
    escaped = []
    for keyword in keywords:
        token = keyword.strip().lower()
        if not token:
            continue
        escaped.append(re.escape(token).replace(r"\ ", r"\s+"))
    if not escaped:
        return r"a^"
    return r"(?i)(?:^|[^a-z0-9])(" + "|".join(escaped) + r")(?:[^a-z0-9]|$)"


def contains_keyword(text: str | None, keywords: list[str]) -> bool:
    """Return True when text contains any configured keyword or phrase."""
    if not text:
        return False
    return re.search(keyword_pattern(keywords), text) is not None
