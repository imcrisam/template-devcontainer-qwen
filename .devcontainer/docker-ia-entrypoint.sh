#!/bin/bash
set -e

# MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-Q3_K_M.gguf"
MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-UD-IQ3_XXS.gguf" #max context 262144

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
  --port 8080 \
  --host 0.0.0.0\
  --ctx-size 15000\
  --n-gpu-layers 44 \
  --n-predict 1014 \
  --threads -1 \
  --flash-attn auto \
  --verbose-prompt \
  --jinja \
  --no-mmap
  # --chat-template-kwargs "$(cat $PARAMS_PATH)"\
  # --chat-template-file "$TEMPLATE_PATH"\
  # --fim-qwen-30b-default
  # --top-p 0.7 \
  # --temp 0.5 \
  # --top-k 40 \
  # --min-p 0.05 \
  # --repeat-penalty 1.15 \

