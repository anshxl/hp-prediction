import io, matplotlib.pyplot as plt
from .infer import curve_for_map

def plot_map_curve_png(map_name: str) -> bytes:
    df = curve_for_map(map_name).sort_values("ScoreDiff_P4")
    x = df["ScoreDiff_P4"].values
    y = df["WinProb_Team1"].values
    lo = df["CI_low"].values
    hi = df["CI_high"].values

    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(x, y, lw=2)
    ax.fill_between(x, lo, hi, alpha=0.2)
    ax.axhline(0.5, ls=":", lw=1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("ScoreDiff_P4 (Team1 - Team2)")
    ax.set_ylabel("Win Probability (Team1)")
    ax.set_title(f"Win Probability after P4 — {map_name}")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=125, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
