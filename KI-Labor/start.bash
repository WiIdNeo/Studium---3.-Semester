lms server start --cors --bind 0.0.0.0
llama-server -hf unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M --jinja -c 8192 --port 8080
# Rebuild
mkdir -p ~/.local/bin
ln -sf "$PWD/build/bin/llama-server" ~/.local/bin/llama-server
ln -sf "$PWD/build/bin/llama-cli" ~/.local/bin/llama-cli
ln -sf "$PWD/build/bin/llama-bench" ~/.local/bin/llama-bench
ln -sf "$PWD/build/bin/rpc-server" ~/.local/bin/rpc-server


docker start open-webui

uvx duckduckgo-mcp-server --transport streamable-http --host 0.0.0.0 --port 8000
