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
