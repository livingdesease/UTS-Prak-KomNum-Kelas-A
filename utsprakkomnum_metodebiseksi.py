    # Anggota 1 (Mellani Sofie) — import, evaluator fungsi, dan hitung_f()

import tkinter as tk
from tkinter import ttk, messagebox
import math
import ast
import operator


# Evaluator fungsi matematika yang membatasi operasi yang diperbolehkan.
# Bisa menggunakan x^2 atau x**2, sin(x), cos(x), sqrt(x), log(x), dan sebagainya.
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_ALLOWED_UNARYOPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_ALLOWED_FUNCS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
    "exp": math.exp, "abs": abs,
}
_ALLOWED_CONSTS = {"pi": math.pi, "e": math.e}

DEFAULT_INPUT = {"rumus": "0", "a": "0", "b": "0", "e": "0", "N": "0"}


def _eval_node(node, x):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, x)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id == "x":
            return x
        if node.id in _ALLOWED_CONSTS:
            return _ALLOWED_CONSTS[node.id]
        raise ValueError(f"Nama '{node.id}' tidak dikenal.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left, x)
        right = _eval_node(node.right, x)
        return _ALLOWED_BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_eval_node(node.operand, x))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        if name not in _ALLOWED_FUNCS or len(node.args) != 1 or node.keywords:
            raise ValueError("Fungsi tidak didukung atau format fungsi salah.")
        return _ALLOWED_FUNCS[name](_eval_node(node.args[0], x))
    raise ValueError("Rumus mengandung operasi yang tidak didukung.")


def hitung_f(rumus, x):
    rumus = rumus.replace("^", "**")
    tree = ast.parse(rumus, mode="eval")
    hasil = _eval_node(tree, x)
    if not math.isfinite(float(hasil)):
        raise ValueError(f"Nilai fungsi tidak valid pada x = {x}.")
    return float(hasil)

# Anggota 2 (Muhammad Khishal Ardana) — fungsi metode_biseksi()


def metode_biseksi(rumus, a, b, toleransi, iterasi_maks):
    fa_awal = hitung_f(rumus, a)
    fb_awal = hitung_f(rumus, b)

    if fa_awal * fb_awal > 0:
        raise ValueError(
            "f(a) dan f(b) harus memiliki tanda yang berbeda, "
            "atau salah satu batas harus merupakan akar.\\n"
            f"Saat ini f(a) = {fa_awal:.6g} dan f(b) = {fb_awal:.6g}."
        )

    data = []
    akar = None

    # Selalu jalankan sebanyak N iterasi yang diminta pengguna.
    # Toleransi dan akar eksak dicatat sebagai informasi, tetapi tidak
    # menghentikan pengisian tabel sebelum jumlah iterasi terpenuhi.
    for i in range(1, iterasi_maks + 1):
        fa = hitung_f(rumus, a)
        fb = hitung_f(rumus, b)
        xr = (a + b) / 2
        fxr = hitung_f(rumus, xr)
        produk = fxr * fa
        selisih = abs(b - a)

        data.append([i, a, b, fa, fb, xr, fxr, produk, selisih])
        akar = xr
        
        # Jika fxr tepat nol, tetap lanjutkan pengisian tabel sampai N.
        # Interval berikutnya dipersempit dari sisi a agar iterasi berikut
        # tetap dapat dihitung dan jumlah baris sesuai input.
        if produk < 0:
            b = xr
        else:
            a = xr

    if any(row[6] == 0 for row in data):
        iterasi_akar = next(row[0] for row in data if row[6] == 0)
        alasan = (
            f"Akar eksak ditemukan pada iterasi ke-{iterasi_akar}. "
            f"Tabel tetap ditampilkan sampai N = {iterasi_maks}."
        )
    elif data[-1][8] < toleransi:
        alasan = (
            f"Toleransi error terpenuhi pada iterasi terakhir "
            f"(|b-a| = {data[-1][8]:.6g} < {toleransi:g}). "
            f"Tabel menampilkan N = {iterasi_maks} iterasi."
        )
    else:
        alasan = (
            f"Seluruh {iterasi_maks} iterasi selesai. "
            f"Toleransi error belum terpenuhi."
        )

    return akar, alasan, data

# Anggota 3 (Hermanda Saputra) — class AplikasiBiseksi dan tampilan GUI


class AplikasiBiseksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Metode Biseksi")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg="#F3F6FB")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#E6ECF5")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TEntry", padding=7)

        header = tk.Frame(root, bg="#172554", padx=24, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="KALKULATOR METODE BISEKSI", bg="#172554",
                 fg="white", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(header, text="Metode numerik untuk mencari akar persamaan f(x) = 0",
                 bg="#172554", fg="#CBD5E1", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(root, bg="#F3F6FB", padx=20, pady=16)
        body.pack(fill="both", expand=True)

        input_card = tk.Frame(body, bg="white", padx=18, pady=16,
                              highlightbackground="#D9E2F0", highlightthickness=1)
        input_card.pack(fill="x")
        tk.Label(input_card, text="Input Perhitungan", bg="white", fg="#172554",
                 font=("Segoe UI", 13, "bold")).grid(row=0, column=0, columnspan=5,
                                                      sticky="w", pady=(0, 12))
