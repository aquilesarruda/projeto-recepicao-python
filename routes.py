from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from utils import (
    datetime,
    salvar_dados,
    carregar_dados,
    atualizar_status,
    alternar_chamado,
    get_nome_arquivo,
    get_available_csvs,
    get_csv_summary,
)
import re
from pathlib import Path

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"


@app.route("/")
def home():
    nome_do_csv = get_nome_arquivo()
    if not nome_do_csv:
        flash("Nenhum arquivo CSV disponível.", "danger")
        registros = []
    else:
        registros = carregar_dados(nome_do_csv) or []
    return render_template("index.html", registros=registros)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/recepcao", methods=["GET", "POST"])
def recepcao():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        atendimento = request.form.get("atendimento", "").strip()
        bairro = request.form.get("bairro", "").strip()

        if not nome or not cpf or not atendimento or not bairro:
            flash("Por favor, preencha todos os campos.", "warning")
        else:
            dados = {
                "nome": nome,
                "cpf": cpf,
                "atendimento": atendimento,
                "bairro": bairro,
            }
            try:
                salvar_dados(dados)
                flash("Dados salvos com sucesso!", "success")
            except Exception as e:
                flash(f"Erro ao salvar dados: {e}", "danger")

        return redirect(url_for("recepcao"))

    # Método GET
    nome_do_csv = get_nome_arquivo()
    registros = carregar_dados(nome_do_csv) or []

    # Ordenar do mais recente para o mais antigo
    try:

        def extrair_data(r):
            data = r.get("Data")
            if isinstance(data, datetime):
                return data
            elif isinstance(data, str):
                try:
                    return datetime.strptime(data, "%d-%m-%Y %H:%M")
                except ValueError:
                    return datetime.min  # data inválida
            return datetime.min

        registros.sort(key=extrair_data, reverse=True)
    except Exception as e:
        flash(f"Erro ao ordenar registros: {e}", "danger")

    return render_template("index.html", registros=registros)


@app.route("/chamar/<id_registro>/<estado_atual>", methods=["POST"])
def chamar(id_registro, estado_atual):
    nome_do_csv = get_nome_arquivo()
    if nome_do_csv:
        alternar_chamado(id_registro, estado_atual, nome_do_csv)
        flash("Status de chamado atualizado com sucesso.", "success")
    else:
        flash("Erro ao atualizar status de chamado.", "danger")
    return redirect(url_for("recepcao"))


@app.route("/atualizar/<id_registro>", methods=["POST"])
def atualizar(id_registro):
    estado_atual = request.form.get("chamado_atual")

    if estado_atual not in ("Sim", "Não", "Nao"):
        flash("Valor de chamado inválido.", "danger")
        return redirect(url_for("recepcao"))

    nome_do_csv = get_nome_arquivo()
    if nome_do_csv:
        atualizar_status(id_registro, nome_do_csv)
        alternar_chamado(id_registro, estado_atual, nome_do_csv)
        flash("Status atualizado com sucesso.", "success")
    else:
        flash("Erro ao atualizar status.", "danger")

    return redirect(url_for("recepcao"))


@app.route("/relatorio", methods=["GET"])
def relatorio():
    arquivos_disponiveis = get_available_csvs() or []
    selected_file = request.args.get("arquivo") or get_nome_arquivo()

    # Verifica se o arquivo selecionado está na lista disponível
    if not selected_file or selected_file not in arquivos_disponiveis:
        flash("Arquivo não encontrado ou inválido.", "danger")
        return render_template(
            "relatorio_recepcao.html",
            registros=[],
            arquivos_disponiveis=arquivos_disponiveis,
            arquivo_atual=None,
            summary=None,
            mes_ano_formatado="Data desconhecida",
        )

    registros = carregar_dados(selected_file)
    summary = get_csv_summary(selected_file)

    # Extrai ano e mês do nome do arquivo
    nome_arquivo = Path(selected_file).stem
    match = re.search(r"(\d{4})-(\d{2})", nome_arquivo)
    if match:
        ano, mes = match.groups()
        mes_ano_formatado = f"{mes}-{ano}"
    else:
        mes_ano_formatado = "Data desconhecida"

    return render_template(
        "relatorio_recepcao.html",
        registros=registros,
        arquivos_disponiveis=arquivos_disponiveis,
        arquivo_atual=selected_file,
        summary=summary,
        mes_ano_formatado=mes_ano_formatado,
    )


@app.template_filter("formatar_cpf")
def formatar_cpf(cpf):
    # Remove tudo que não for número
    cpf_numeros = "".join(filter(str.isdigit, str(cpf)))[:11]

    if len(cpf_numeros) == 11:
        return (
            f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        )
    return cpf  # Caso esteja incompleto ou inv�lido