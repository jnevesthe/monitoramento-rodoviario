<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Detalhes do Veículo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        :root {
            --primary-color: #003366;
            --accent-color: #00509e;
            --danger-color: #cc0000;
            --bg-body: #eef2f7;
            --card-white: #ffffff;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background-color: var(--bg-body); padding: 20px; color: #222; }

        h1 { color: var(--primary-color); text-align: center; margin-bottom: 20px; }
        h2 { color: var(--primary-color); margin-bottom: 10px; }

        .veiculo {
            background: var(--card-white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.08);
            border: 1px solid #d1d5db;
            margin-bottom: 30px;
        }

        .card-header {
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            padding: 20px;
            color: white;
        }

        .prop-nome { font-size: 1.2rem; font-weight: 800; display: block; margin-bottom: 2px; }
        .prop-cidade { font-size: 0.8rem; opacity: 0.9; display: block; margin-bottom: 12px; }

        .veiculo-info-linha {
            background: rgba(255,255,255,0.15);
            padding: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .veiculo-texto { font-size: 0.9rem; font-weight: 600; }
        .placa-pill {
            background: white; color: var(--primary-color);
            padding: 4px 10px; border-radius: 6px; font-family: monospace; font-weight: 900;
        }

        .card-body { padding: 20px; }

        .secao-titulo {
            font-size: 0.75rem; color: #64748b; font-weight: 800;
            text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.5px;
        }

        .multa {
            background: #fff1f2; border-left: 4px solid var(--danger-color);
            padding: 12px; border-radius: 6px; margin-bottom: 8px;
        }

        .multa-valor { color: var(--danger-color); font-weight: 800; font-size: 1rem; }
        .multa-meta { display: block; font-size: 0.75rem; color: #7f8c8d; margin-top: 4px; }

        .btn-multar {
            display: block; width: 100%; background: var(--danger-color);
            color: white; text-align: center; padding: 15px; border-radius: 12px;
            text-decoration: none; font-weight: 800; margin-top: 15px;
            transition: transform 0.2s;
        }

        .btn-multar:active { transform: scale(0.97); }

        a.voltar { text-decoration: none; color: var(--primary-color); font-weight: bold; display: inline-block; margin-top: 20px; }
    </style>
</head>
<body>

<h1>Detalhes do Veículo</h1>

<div class="veiculo">
    <header class="card-header">
        <span class="prop-nome">{{ veiculo.proprietario.nome_completo }}</span>
        <span class="prop-cidade">📍 {{ veiculo.proprietario.cidade }}</span>
        <div class="veiculo-info-linha">
            <span class="veiculo-texto">{{ veiculo.marca }} {{ veiculo.modelo }} ({{ veiculo.cor }})</span>
            <span class="placa-pill">{{ veiculo.matricula }}</span>
        </div>
    </header>

    <div class="card-body">
        <p class="secao-titulo">Multas do Veículo</p>

        {% if veiculo.multas.all %}
            {% for m in veiculo.multas.all %}
            <div class="multa">
                <span class="multa-valor">R$ {{ m.valor }}</span>
                <span style="font-size: 0.85rem; color: #1e293b; margin-left: 5px;">| {{ m.localizacao }}</span>
                <span class="multa-meta">📅 {{ m.data|date:"d/m/Y H:i" }} • Agente: {{ m.agente }}</span>
            </div>
            {% endfor %}
        {% else %}
            <p style="color: #10b981; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px;">✅ Sem multas registradas.</p>
        {% endif %}

        <a href="{% url 'multar' veiculo.id %}" class="btn-multar">🚨 APLICAR MULTA</a>
    </div>
</div>

<a href="{% url 'list' %}" class="voltar">&larr; Voltar para Lista</a>

</body>
</html>
