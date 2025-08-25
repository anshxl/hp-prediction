from typing import Dict

# Map -> Datawrpper ID
MAP_TO_DW: Dict[str, str] = {
    "Apocalypse": "vErQr",
    "Combine": "qiJ7j",
    "Hacienda": "3apmr",
    "Slums": "r6DyA",
    "Summit": "howjs",
}

def iframe_html_for_map(map_name: str) -> str:
    if map_name not in MAP_TO_DW:
        raise ValueError(f"Unknown map: {map_name}")
    chart_id = MAP_TO_DW[map_name]
    return (
        f'<iframe title="HP Win Prob - {map_name}" '
        f'aria-label="Line chart" id="datawrapper-chart-{chart_id}" '
        f'src="https://datawrapper.dwcdn.net/{chart_id}/3/" '
        f'scrolling="no" frameborder="0" style="border: none;" width="600" height="421" data-external="1"></iframe>'
    )
