#!/bin/bash
# Jalankan dari folder yang berisi server.py, client.py, dan log_processor.py
# Contoh: cd ~/k1-ipc-kelompok7 && bash kumpulkan_data_uji.sh
cd "$(dirname "$0")" || exit 1

if ss -ltn 2>/dev/null | grep -q ':5050 '; then
  echo "Port 5050 sedang dipakai. Hentikan server.py yang berjalan (Ctrl+C) lalu ulangi."
  exit 1
fi

echo "=== SPESIFIKASI VM ==="
echo "Hostname : $(hostname)"
echo "OS       : $(. /etc/os-release && echo "$PRETTY_NAME")"
echo "Kernel   : $(uname -r)"
echo "vCPU     : $(nproc)"
echo "RAM      : $(free -h | awk '/^Mem:/ {print $2}')"
echo "Python   : $(python3 --version)"
echo

echo "=== UJI 4: klien dijalankan saat server mati ==="
printf 'IF-IIIA\nRabu\n' | python3 client.py
echo

echo "=== UJI 5: pesan tanpa pemisah | ==="
python3 -u server.py > /tmp/server_uji.log 2>&1 &
SP=$!
sleep 1
python3 - <<'PY'
import socket
s = socket.create_connection(("127.0.0.1", 5050), timeout=5)
s.sendall(b"IF-IIIA")
print("Jawaban server:", s.recv(1024).decode())
s.close()
PY
sleep 1
kill "$SP" 2>/dev/null
wait "$SP" 2>/dev/null
echo
echo "--- Keluaran server selama uji 5 ---"
cat /tmp/server_uji.log
