import csv
from pathlib import Path
from datetime import datetime

DADOS_FOLDER = Path("dados")
DADOS_FOLDER.mkdir(exist_ok=True)

def get_nome_arquivo():
    # Retorna o arquivo do mês atual, ex: "dados/2025_09.csv"
    hoje = datetime.now()
    nome_arquivo = f"{hoje.year}_{hoje.month:02d}.csv"
    return str(DADOS_FOLDER / nome_arquivo)

def get_available_csvs():
    return [str(f) for f in sorted(DADOS_FOLDER.glob("*.csv"), reverse=True)]

def carregar_dados(nome_arquivo):
    path = Path(nome_arquivo)
    if not path.exists():
        return []
    registros = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Converter campos conforme necessidade
            row["ID"] = row.get("ID", "")
            row["Nome"] = row.get("Nome", "")
            row["CPF"] = row.get("CPF", "")
            row["Atendimento"] = row.get("Atendimento", "")
            row["Bairro"] = row.get("Bairro", "")
            row["Chamado"] = row.get("Chamado", "Não")
            row["Status"] = row.get("Status", "Pendente")
            data_str = row.get("Data", "")
            try:
                row["Data"] = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
            except Exception:
                row["Data"] = datetime.now()
            registros.append(row)
    return registros

def salvar_dados(dados):
    nome_arquivo = get_nome_arquivo()
    path = Path(nome_arquivo)
    criar_arquivo = not path.exists()

    campos = ["ID", "Data", "Nome", "CPF", "Atendimento", "Bairro", "Chamado", "Status"]

    registros = carregar_dados(nome_arquivo)
    ultimo_id = 0
    if registros:
        try:
            ultimo_id = max(int(r["ID"]) for r in registros if r["ID"].isdigit())
        except Exception:
            ultimo_id = 0

    novo_id = ultimo_id + 1
    linha = {
        "ID": str(novo_id),
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nome": dados.get("nome", ""),
        "CPF": dados.get("cpf", ""),
        "Atendimento": dados.get("atendimento", ""),
        "Bairro": dados.get("bairro", ""),
        "Chamado": "Não",
        "Status": "Pendente",
    }

    with open(nome_arquivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if criar_arquivo:
            writer.writeheader()
        writer.writerow(linha)

def atualizar_status(id_registro, nome_arquivo):
    registros = carregar_dados(nome_arquivo)
    atualizado = False
    for r in registros:
        if r["ID"] == id_registro:
            r["Status"] = "OK"
            atualizado = True
            break
    if atualizado:
        salvar_todos_registros(registros, nome_arquivo)

def alternar_chamado(id_registro, estado_atual, nome_arquivo):
    registros = carregar_dados(nome_arquivo)
    atualizado = False
    for r in registros:
        if r["ID"] == id_registro:
            if estado_atual.lower() == "sim":
                r["Chamado"] = "Não"
            else:
                r["Chamado"] = "Sim"
            atualizado = True
            break
    if atualizado:
        salvar_todos_registros(registros, nome_arquivo)

def salvar_todos_registros(registros, nome_arquivo):
    campos = ["ID", "Data", "Nome", "CPF", "Atendimento", "Bairro", "Chamado", "Status"]
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in registros:
            if isinstance(r["Data"], datetime):
                r["Data"] = r["Data"].strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(r)

def get_csv_summary(nome_arquivo):
    registros = carregar_dados(nome_arquivo)
    total = len(registros)
    chamados_sim = sum(1 for r in registros if r["Chamado"].lower() == "sim")
    chamados_nao = total - chamados_sim
    return {
        "total": total,
        "chamados_sim": chamados_sim,
        "chamados_nao": chamados_nao,
    }
