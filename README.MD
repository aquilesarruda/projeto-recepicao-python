Sistema de Recepção - Controle de Atendimentos

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)
![License](https://img.shields.io/badge/Licença-MIT-green)

> Sistema web para registro e controle de atendimentos com exportação mensal em CSV.

---

##Funcionalidades

-Cadastro de atendimentos com:
  - Nome
  - CPF (validação e formatação automática)
  - Tipo de atendimento
  - Bairro

 Armazenamento automático em arquivos CSV por mês (`dados/YYYY-MM.csv`)
 Relatórios com:
  - Contagem por atendimento e bairro
  - Filtro por mês (arquivo)
  - Totais e chamados Sim/Não

 Registros exibidos do **mais recente para o mais antigo**
 Interface moderna, responsiva e leve (Bootstrap 5 + CSS customizado)

---

## Estrutura do Projeto

```

seu_projeto/
├── app/
│   ├── **init**.py
│   ├── routes.py
│   ├── utils.py
│
├── templates/
│   ├── index.html
│   └── relatorio_recepcao.html
│
├── static/
│   ├── style.css
│   └── images/
│
├── dados/
│   └── (Arquivos CSV gerados automaticamente)
│
├── run.py
├── requirements.txt
└── README.md

````

---

#Instalação Local

1. **Clone ou extraia o projeto**

```bash
git clone https://github.com/seuusuario/seu-repo.git
cd seu-repo
````

2. **Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/macOS
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**

```bash
python run.py
```

5. Acesse em http://localhost:5000/

---

##Deploy em Produção

### Heroku

1. Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Crie um `Procfile` com:

```
web: python run.py
```

3. Faça o deploy com:

```bash
heroku login
heroku create seu-app
git push heroku main
```

### Railway (mais simples)

1. Crie uma conta em [https://railway.app](https://railway.app)
2. Crie um novo projeto e conecte seu repositório GitHub
3. Railway detecta o `requirements.txt` automaticamente
4. Configure o comando de start:

```bash
python run.py
```

---

##Exportação dos Dados

Os dados são salvos em tempo real em `dados/YYYY-MM.csv`.
Você pode abrir, editar ou importar em planilhas normalmente.

---

## Requisitos

* Python 3.8+
* Flask
* Pandas

Verifique todas as dependências em: `requirements.txt`

---

##Autor

**Aquiles Silva Arruda**
© 2025 – Todos os direitos reservados.

---

#Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

```
