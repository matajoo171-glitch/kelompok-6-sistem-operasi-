import socket

HOST = "127.0.0.1"
PORT = 5050

def main():
    kelas = input("Masukkan kelas (contoh IF-IIIA): ").strip()
    hari = input("Masukkan hari (contoh Rabu): ").strip()

    permintaan = f"{kelas}|{hari}"

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as client:
            client.sendall(permintaan.encode("utf-8"))
            jawaban = client.recv(4096).decode("utf-8")

        print("\n=== HASIL CEK JADWAL ===")
        print(jawaban)

    except OSError as error:
        print(f"Gagal terhubung ke server: {error}")
        print("Pastikan server.py sedang berjalan.")

if __name__ == "__main__":
    main()
