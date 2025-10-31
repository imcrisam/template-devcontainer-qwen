#!/bin/bash
set -e

# MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-Q3_K_M.gguf"
# MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-UD-IQ3_XXS.gguf" #max context 262144
MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-UD-IQ1_S.gguf" #max context 262144

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

exec ./llama-server \
  --model "$MODEL_PATH" \
  -v \
  --ctx-size 48000 \
  --n-gpu-layers 56 \
  --threads -1 \
  --flash-attn auto \
  --props \
  --temp 0.7 --min-p 0.01 --top-p 0.8 --top-k 20 --presence-penalty 1.05 \
  --repeat-penalty 1.25 \
  --jinja \
  --chat-template-file "qwen3_code_15012.jinja" \
  --cache-ram 0 \
  --host 0.0.0.0 --port 8080
  # --verbose-prompt \
  # --n-predict 1014 \
  # --no-mmap \

