"""
📘 Study Session Logger
Uses Ebbinghaus Forgetting Curve + SM-2 Spaced Repetition Algorithm
"""

import json
import math
import os
from datetime import datetime, timedelta

DATA_FILE = "study_sessions.json"

# ── Persistence ────────────────────────────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}   # { "subject::topic": { card data } }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Ebbinghaus Forgetting Curve ────────────────────────────────────────────────
#   R = e^(-t / S)
#   R  = retention (0–1)
#   t  = days since last study
#   S  = memory stability (grows with each successful review)

def retention_now(stability: float, days_elapsed: float) -> float:
    """Current estimated retention (0–100%)."""
    if stability <= 0:
        return 0.0
    return math.exp(-days_elapsed / stability) * 100

# ── SM-2 Interval Calculation ──────────────────────────────────────────────────
#   quality: 0–5  (derived from focus + fatigue)
#   EF (ease factor) adjusts how quickly intervals grow

def quality_from_session(focus: int, fatigue: bool) -> int:
    """Map focus + fatigue to SM-2 quality score (0–5)."""
    q = focus  # focus 1-5 maps loosely to quality 1-5
    if fatigue:
        q = max(0, q - 1)
    return min(q, 5)

def update_sm2(card: dict, quality: int) -> dict:
    """
    Apply SM-2 algorithm to a card and return updated card.
    card keys: interval, repetitions, ease_factor, stability
    """
    EF = card.get("ease_factor", 2.5)
    interval = card.get("interval", 1)
    reps = card.get("repetitions", 0)
    stability = card.get("stability", 1.0)

    if quality >= 3:                          # successful recall
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * EF)
        reps += 1
        stability = stability * (1 + 0.2 * (quality - 3))   # grows on success
        stability = max(stability, 0.5)
    else:                                     # failed recall → reset
        interval = 1
        reps = 0
        stability = max(stability * 0.5, 0.5)               # decays on failure

    EF = EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    EF = max(EF, 1.3)                         # EF never drops below 1.3

    card.update({
        "interval": interval,
        "repetitions": reps,
        "ease_factor": round(EF, 2),
        "stability": round(stability, 2),
        "last_reviewed": datetime.now().isoformat(),
        "next_review": (datetime.now() + timedelta(days=interval)).isoformat()
    })
    return card

# ── Display Helpers ────────────────────────────────────────────────────────────

def fmt_date(iso: str) -> str:
    return datetime.fromisoformat(iso).strftime("%d %b %Y")

def days_until(iso: str) -> int:
    delta = datetime.fromisoformat(iso) - datetime.now()
    return max(0, delta.days)

def retention_bar(pct: float, width: int = 20) -> str:
    filled = round(pct / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    color = "🟢" if pct >= 70 else "🟡" if pct >= 40 else "🔴"
    return f"{color} [{bar}] {pct:.1f}%"

def print_card_summary(key: str, card: dict):
    subject, topic = key.split("::", 1)
    last = card.get("last_reviewed")
    nxt  = card.get("next_review")

    days_elapsed = (datetime.now() - datetime.fromisoformat(last)).total_seconds() / 86400 if last else 0
    ret = retention_now(card.get("stability", 1.0), days_elapsed)
    due_in = days_until(nxt) if nxt else 0
    overdue = due_in == 0 and last is not None

    print(f"\n  📚 {subject}  ›  {topic}")
    print(f"     Retention     : {retention_bar(ret)}")
    print(f"     Interval      : every {card.get('interval', '?')} day(s)   |   Reps: {card.get('repetitions', 0)}")
    print(f"     Ease Factor   : {card.get('ease_factor', 2.5)}")
    if nxt:
        status = "⚠️  OVERDUE" if overdue else f"in {due_in} day(s)"
        print(f"     Next Review   : {fmt_date(nxt)}  ({status})")

# ── Menus ──────────────────────────────────────────────────────────────────────

def log_session(data: dict):
    print("\n── New Session ───────────────────────────────")
    subject  = input("  Subject     : ").strip()
    topic    = input("  Topic       : ").strip()
    duration = int(input("  Minutes studied : "))
    focus    = int(input("  Focus level (1–5): "))
    fatigue  = input("  Feeling tired? (yes/no): ").strip().lower() == "yes"

    key = f"{subject}::{topic}"
    card = data.get(key, {
        "interval": 1, "repetitions": 0,
        "ease_factor": 2.5, "stability": 1.0,
        "history": []
    })

    quality = quality_from_session(focus, fatigue)
    card = update_sm2(card, quality)

    # Append to history
    card.setdefault("history", []).append({
        "date": datetime.now().isoformat(),
        "duration": duration,
        "focus": focus,
        "fatigue": fatigue,
        "quality": quality,
        "retention_at_study": round(retention_now(
            card["stability"], 0), 1)     # retention right after studying ≈ 100%
    })

    data[key] = card
    save_data(data)

    # Feedback
    print("\n── Session Saved ─────────────────────────────")
    if quality >= 4 and not fatigue:
        print("  ✅ Excellent session! Interval extended significantly.")
    elif quality == 3:
        print("  👍 Good effort. Keep the momentum going.")
    elif fatigue:
        print("  😴 Fatigue detected. Rest — recall under fatigue weakens long-term memory.")
    else:
        print("  ⚠️  Low focus session. Interval reset to rebuild the memory trace.")

    print(f"\n  SM-2 Quality Score : {quality}/5")
    print(f"  New Interval       : {card['interval']} day(s)")
    print(f"  Next Review        : {fmt_date(card['next_review'])}")
    print(f"  Memory Stability   : {card['stability']}")

def show_dashboard(data: dict):
    if not data:
        print("\n  No sessions logged yet.")
        return

    print("\n── Dashboard ─────────────────────────────────")
    due_today = []
    upcoming  = []

    for key, card in data.items():
        nxt = card.get("next_review")
        if not nxt:
            continue
        if days_until(nxt) == 0:
            due_today.append((key, card))
        else:
            upcoming.append((key, card))

    if due_today:
        print(f"\n  🔔 Due for Review ({len(due_today)} topic(s)):")
        for key, card in due_today:
            print_card_summary(key, card)

    if upcoming:
        upcoming.sort(key=lambda x: x[1].get("next_review", ""))
        print(f"\n  📅 Upcoming Reviews:")
        for key, card in upcoming:
            print_card_summary(key, card)

def show_history(data: dict):
    if not data:
        print("\n  No sessions logged yet.")
        return

    print("\n── Session History ───────────────────────────")
    for key, card in data.items():
        subject, topic = key.split("::", 1)
        print(f"\n  {subject} › {topic}  ({len(card.get('history', []))} session(s))")
        for entry in card.get("history", []):
            date_str = datetime.fromisoformat(entry["date"]).strftime("%d %b %Y %H:%M")
            fatigue_tag = "😴" if entry.get("fatigue") else ""
            print(f"    {date_str}  |  {entry['duration']}min  |  "
                  f"Focus: {entry['focus']}/5  |  Quality: {entry['quality']}/5  {fatigue_tag}")

# ── Main Loop ──────────────────────────────────────────────────────────────────

def main():
    data = load_data()

    print("╔══════════════════════════════════════════╗")
    print("║      📘 Spaced Repetition Study Logger   ║")
    print("╚══════════════════════════════════════════╝")

    while True:
        print("\n  1. Log a study session")
        print("  2. View dashboard (due reviews + retention)")
        print("  3. View session history")
        print("  4. Quit")
        choice = input("\n  Choose (1–4): ").strip()

        if choice == "1":
            log_session(data)
        elif choice == "2":
            show_dashboard(data)
        elif choice == "3":
            show_history(data)
        elif choice == "4":
            print("\n  See you next review! 👋\n")
            break
        else:
            print("  Invalid choice, try again.")

if __name__ == "__main__":
    main()


