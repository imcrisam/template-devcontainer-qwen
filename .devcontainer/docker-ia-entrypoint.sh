#!/bin/bash
set -e

MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-Q3_K_M.gguf"

MODEL_PATH="/models/$MODEL_NAME"
MODEL_URL="https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF/resolve/main/$MODEL_NAME"

mkdir -p /models

if [ ! -f "$MODEL_PATH" ]; then
  echo "Downloading model..."
  curl -L --progress-bar -o "$MODEL_PATH" "$MODEL_URL"
else
  echo "Model already exists at $MODEL_PATH"
fi

TEMPLATE_PATH="/models/chat_template.jinja"
TEMPLATE_URL="https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF/resolve/main/template"

if [ ! -f "$TEMPLATE_PATH" ]; then
  echo "Downloading chat template..."
  curl -L --progress-bar -o "$TEMPLATE_PATH" "$TEMPLATE_URL"
else
  echo "Chat template already exists at $TEMPLATE_PATH"
fi

PARAMS_PATH="/models/chat_params.json"
PARAMS_URL="https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF/resolve/main/params"

if [ ! -f "$PARAMS_PATH" ]; then
  echo "Downloading chat params..."
  curl -L --progress-bar -o "$PARAMS_PATH" "$PARAMS_URL"
else
  echo "Chat params already exist at $PARAMS_PATH"
fi

./llama-server --list-devices

exec ./llama-server \
  --model "$MODEL_PATH" \
  -v \
  --threads -1 \
  --chat-template-file "$TEMPLATE_PATH"\
  --chat-template-kwargs "$(cat $PARAMS_PATH)"\
  --jinja \
  --no-mmap \
  --ctx-size 15000 \
  --n-gpu-layers 48 \
  --n-predict 1014 \
  --verbose-prompt \
  --port 8080 \
  --host 0.0.0.0

  # --flash-attn auto \

# --ctx-size 15000 (un valor más alto mejora la calidad de los resultados, pero requiere más memoria VRAM y RAM)
# --n-gpu-layers 48 (un valor más alto utiliza más VRAM, pero ofrece mejor rendimiento; un valor más bajo consume menos VRAM, pero puede requerir más RAM)

# --ctx-size 15000 (a higher value improves result quality but requires more VRAM and RAM)
# --n-gpu-layers 48 (a higher value uses more VRAM but offers better performance; a lower value consumes less VRAM but may require more RAM)
