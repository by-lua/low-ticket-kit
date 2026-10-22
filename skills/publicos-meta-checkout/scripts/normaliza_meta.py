#!/usr/bin/env python3
"""Normaliza export do checkout (CSV ou XLSX) para o formato de público personalizado do Meta.

Uso:
  python3 normaliza_meta.py <entrada.csv|xlsx> <saida.csv> [--excluir <lista.csv|xlsx>]

Detecta as colunas pelo cabeçalho (sem diferenciar caixa/acento/espaço):
  e-mail: email, e-mail, e_mail, customer email, client.email ...
  telefone: phone, telefone, celular, whatsapp, client.phone ...
  nome: name, nome, customer name, client.name ...
Saída: email, phone (DDI 55, só dígitos), fn, ln, ct, st, country=br. Deduplicado por e-mail.

XLSX é lido só com a biblioteca padrão (zipfile + xml): primeira aba, primeira linha = cabeçalho.
"""
import csv
import re
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ALIAS = {
    "email": ["email", "e mail", "e_mail", "mail", "customer email", "client email", "client.email", "email do cliente"],
    "phone": ["phone", "telefone", "celular", "whatsapp", "fone", "client phone", "client.phone", "telefone do cliente"],
    "name": ["name", "nome", "customer name", "client name", "client.name", "nome do cliente"],
}


def norm(texto):
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t.strip().lower())


def le_xlsx(caminho):
    with zipfile.ZipFile(caminho) as z:
        comuns = []
        if "xl/sharedStrings.xml" in z.namelist():
            raiz = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in raiz.findall("m:si", NS):
                comuns.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        folha = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        linhas = []
        for row in folha.iter("{%s}row" % NS["m"]):
            valores = {}
            for c in row.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                idx = 0
                for ch in ref:
                    idx = idx * 26 + (ord(ch) - 64)
                v = c.find("m:v", NS)
                if c.get("t") == "s" and v is not None:
                    val = comuns[int(v.text)]
                elif c.get("t") == "inlineStr":
                    val = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
                else:
                    val = v.text if v is not None else ""
                valores[idx - 1] = val
            if valores:
                n = max(valores) + 1
                linhas.append([valores.get(i, "") for i in range(n)])
        return linhas


def le_tabela(caminho):
    if caminho.lower().endswith((".xlsx", ".xlsm")):
        return le_xlsx(caminho)
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        amostra = f.read(4096)
        f.seek(0)
        try:
            dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        except csv.Error:
            dialeto = csv.excel
        return [linha for linha in csv.reader(f, dialeto) if any(c.strip() for c in linha)]


def acha_coluna(cabecalho, grupo):
    nomes = [norm(c) for c in cabecalho]
    for alias in ALIAS[grupo]:
        if alias in nomes:
            return nomes.index(alias)
    for i, nome in enumerate(nomes):
        if any(a in nome for a in ALIAS[grupo]):
            return i
    return None


def tel_br(bruto):
    d = re.sub(r"\D", "", str(bruto or ""))
    if not d:
        return ""
    if d.startswith("55") and len(d) >= 12:
        return d
    # já veio com DDI de outro país (+1..., +351...): mantém
    if str(bruto).strip().startswith("+"):
        return d
    return "55" + d.lstrip("0")


def carrega_emails(caminho):
    linhas = le_tabela(caminho)
    if linhas and any("@" in c for c in linhas[0]):
        # sem cabeçalho: lista de e-mails solta, uma por linha
        return {norm(r[0]) for r in linhas if r and "@" in r[0]}
    ie = acha_coluna(linhas[0], "email")
    return {norm(r[ie]) for r in linhas[1:] if ie is not None and len(r) > ie and "@" in r[ie]}


def main():
    args = sys.argv[1:]
    excluir = set()
    if "--excluir" in args:
        k = args.index("--excluir")
        excluir = carrega_emails(args[k + 1])
        del args[k:k + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    entrada, saida = args

    linhas = le_tabela(entrada)
    cab = linhas[0]
    ie, ip, inome = acha_coluna(cab, "email"), acha_coluna(cab, "phone"), acha_coluna(cab, "name")
    if ie is None:
        sys.exit("Coluna de e-mail não encontrada. Cabeçalho lido: " + " | ".join(cab))
    col = {"email": cab[ie], "phone": cab[ip] if ip is not None else None, "nome": cab[inome] if inome is not None else None}
    print(f"colunas detectadas: {col}")

    vistos = {}
    descartados = 0
    for r in linhas[1:]:
        if len(r) <= ie:
            continue
        email = norm(r[ie])
        if "@" not in email or email in excluir or email in vistos:
            descartados += 1
            continue
        nome = r[inome].strip() if inome is not None and len(r) > inome else ""
        partes = nome.split()
        vistos[email] = {
            "email": email,
            "phone": tel_br(r[ip]) if ip is not None and len(r) > ip else "",
            "fn": norm(partes[0]) if partes else "",
            "ln": norm(partes[-1]) if len(partes) > 1 else "",
            "ct": "",
            "st": "",
            "country": "br",
        }

    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["email", "phone", "fn", "ln", "ct", "st", "country"])
        w.writeheader()
        w.writerows(vistos.values())
    print(f"{len(vistos)} linhas em {saida} (descartadas: {descartados}, sem e-mail válido/duplicadas/excluídas)")


if __name__ == "__main__":
    main()
