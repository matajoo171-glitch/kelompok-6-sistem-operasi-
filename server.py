import socket
import subprocess
import sys
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5050

JADWAL = {
    ("IF-IIIA", "rabu"): [
        "08.00 - 10.29 | Aljabar Vektor dan Matriks | Ruang 10",
        "10.30 - 12.59 | Matematika Diskrit | Ruang 10",
        "14.00 - 16.29 | Statistika dan Probabilitas | Ruang 10"
    ],
    ("IF-IIIA", "kamis"): [
        "08.00 - 10.29 | Pemrograman Berbasis Objek | Lab. Komputer 1",
        "10.30 - 12.59 | Sistem Operasi | Ruang 10",
        "14.00 - 16.29 | Strategi Algoritma | Ruang 10"
    ],
    ("IF-IIIA", "sabtu"): [
        "08.00 - 10.29 | Arsitektur dan Organisasi Komputer | Ruang 10",
        "10.30 - 12.59 | Rekayasa Perangkat Lunak | Ruang 10"
    ],
}

def catat_log(pipe, pesan):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pipe.write(f"{waktu} | {pesan}\n")
    pipe.flush()

def main():
    # stdout server ditampilkan di terminal.
    # stdin log_processor menerima log melalui pipe.
    processor = subprocess.Popen(
        [sys.executable, "-u", "log_processor.py"],
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[SERVER] Berjalan di {HOST}:{PORT}")
        print("[SERVER] Menunggu client...")

        while True:
            conn, alamat = server.accept()

            with conn:
                data = conn.recv(1024).decode("utf-8").strip()
                if not data:
                    continue

                bagian = data.split("|", 1)
                if len(bagian) != 2:
                    jawaban = "Format salah. Gunakan KELAS|HARI."
                    kelas, hari = "-", "-"
                else:
                    kelas = bagian[0].strip().upper()
                    hari = bagian[1].strip().lower()

                    hasil = JADWAL.get((kelas, hari))
                    if hasil:
                        jawaban = (
                            f"Jadwal {kelas} hari {hari.title()}:\n"
                            + "\n".join(hasil)
                        )
                    else:
                        jawaban = (
                            f"Jadwal untuk {kelas} hari "
                            f"{hari.title()} belum tersedia."
                        )

                conn.sendall(jawaban.encode("utf-8"))
                catat_log(
                    processor.stdin,
                    f"client={alamat[0]}:{alamat[1]} "
                    f"kelas={kelas} hari={hari} "
                    f"status={'OK' if 'belum tersedia' not in jawaban else 'TIDAK DITEMUKAN'}"
                )
                print(f"[SERVER] Permintaan {kelas} / {hari}")

    except KeyboardInterrupt:
        print("\n[SERVER] Dihentikan oleh pengguna.")
    finally:
        server.close()
        if processor.stdin:
            processor.stdin.close()
        processor.wait()

if __name__ == "__main__":
    main()
