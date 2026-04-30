#!/bin/sh
mkdir -p .streamlit
python3 -c "
import os
content = os.environ.get('STREAMLIT_SECRETS_TOML', '')
content = content.replace('\\\\n', '\n').replace('\\n', '\n')
open('.streamlit/secrets.toml', 'w').write(content)
"
