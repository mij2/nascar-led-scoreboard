# NASCAR LED Scoreboard — Claude Notes

## Open TODOs

- **Re-enable config validation** (`src/data/scoreboard_config.py`): The `validateConf` import and validation block are currently commented out because the NHL schema (`config/config.schema.json`) does not match the NASCAR config structure. Once `config/config.json` and `config/config.schema.json` are finalized for NASCAR, uncomment the import at the top of the file and the validation block in `__get_config`, then update the warning message (currently references `nhl_setup`).
