#!/bin/sh
mkdir -p .streamlit
printf '%s' "$STREAMLIT_SECRETS_TOML" > .streamlit/secrets.toml
