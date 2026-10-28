# GSA ERM2 MCP Toolkit

A small Python MCP server exposing four tools to Bob and any MCP-compatible client.

## Tools

| Tool | Description |
|---|---|
| `gsa_erm2_current_weather` | Returns live weather for a given location via wttr.in |
| `gsa_erm2_programming_joke` | Fetches a programming joke from JokeAPI |
| `gsa_erm2_unit_converter` | Converts between temperature, length, weight, volume, speed, and time units (local logic) |
| `gsa_erm2_currency_converter` | Converts between currencies using live exchange rates via open.er-api.com (no API key) |

### Unit converter families

| Family | Units |
|---|---|
| Temperature | `celsius`, `fahrenheit`, `kelvin` |
| Length | `m`, `km`, `ft`, `miles` |
| Weight | `kg`, `g`, `lb`, `oz` |
| Volume | `l`, `ml`, `gal` (US), `fl_oz` (US) |
| Speed | `m/s`, `km/h`, `mph`, `knots` |
| Time | `s`, `min`, `h`, `d` |

### Currency converter

Converts any amount between two ISO 4217 currency codes using live rates fetched from
[open.er-api.com](https://open.er-api.com) (free tier, no API key required).

Returns: `amount`, `from_currency`, `result`, `to_currency`, `rate`, `last_updated`.

## Running

```bash
uv run --project . mcp run server.py
```

## Testing

```bash
uv run --with "mcp[cli]>=1.0" --with "httpx>=0.27" --with pytest pytest
```

## Dependencies

- `mcp[cli] >= 1.0`
- `httpx >= 0.27`
- Python >= 3.11
