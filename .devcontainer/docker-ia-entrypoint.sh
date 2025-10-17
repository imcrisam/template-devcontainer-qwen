#!/bin/bash
set -e

MODEL_NAME="Qwen3-Coder-30B-A3B-Instruct-Q3_K_M.gguf"

MODEL_PATH="/models/$MODEL_NAME"
MODEL_URL="https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF/resolve/main/$MODEL_NAME"


mkdir -p /models

if [ ! -f "$MODEL_PATH" ]; then
  echo "Descargando modelo..."
  curl -L --progress-bar -o "$MODEL_PATH" "$MODEL_URL"
else
  echo "Modelo ya existe en $MODEL_PATH"
fi

./llama-server --list-devices

exec ./llama-server \
  --model "$MODEL_PATH" \
  -v \
  --flash-attn auto \
  --fim-qwen-30b-default \
  --ctx-size 15000 \
  --jinja \
  --no-mmap \
  --n-gpu-layers 48 \
  --n-predict 1014 \
  --verbose-prompt \
  --port 8080 \
  --host 0.0.0.0


# --ctx-size 15000 (un valor más alto mejora la calidad de los resultados, pero requiere más memoria VRAM y RAM)
# --n-gpu-layers 48 (un valor más alto utiliza más VRAM, pero ofrece mejor rendimiento; un valor más bajo consume menos VRAM, pero puede requerir más RAM)

# --ctx-size 15000 (a higher value improves result quality but requires more VRAM and RAM)
# --n-gpu-layers 48 (a higher value uses more VRAM but offers better performance; a lower value consumes less VRAM but may require more RAM)
