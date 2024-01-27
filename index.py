from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from dash_bootstrap_templates import ThemeSwitchAIO
from plotly.subplots import make_subplots
import os
from app import *
from database import *


# ========== Styles ============ #
tab_card = {"height": "100%"}

main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "y": 0.9,
        "xanchor": "left",
        "x": 0.1,
        "title": {"text": None},
        "font": {"color": "white"},
        "bgcolor": "rgba(0,0,0,0.5)",
    },
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
}

config_graph = {"displayModeBar": False, "showTips": False}

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div("This is tab 1!", id="card"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
    id="card",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


# Função para criar os cards
def criateCard(code, value, type_):
    pathImage = f"assets/{code}.png"
    defaultImagePath = "https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cindra/imagens/sem.jpg.gif"

    # Verificar se a imagem existe, caso contrário, usar a imagem padrão
    if not os.path.exists(f"{pathImage}"):
        pathImage = defaultImagePath

    integerValue = int(value)
    text_card = (
        html.P(
            f"R${integerValue}", className="card-text", style={"font-size": "0.8rem"}
        )  # 60% do tamanho original
        if type_ == "Preço"
        else html.P(
            f"{integerValue} Peças",
            className="card-text",
            style={"font-size": "0.6rem"},
        )  # 60% do tamanho original
    )
    card_content = [
        dbc.CardImg(
            src=pathImage,
            top=True,
            style={
                "width": "3rem",  # 60% de 4rem
                "height": "3rem",
                "margin-top": "auto",
                "margin-bottom": "auto",  # 60% de 4rem
                "margin-left": "auto",
                "margin-right": "auto",
                "display": "block",
            },
        ),
        dbc.CardBody(
            [
                html.H4(
                    code,
                    className="card-title",
                    style={"font-size": "1rem", "font-weight": "bold"},
                ),
                text_card,
            ]
        ),  
    ]

    return dbc.Card(
        card_content,
        style={
            "height": "8rem", 
            "width": "4.6rem",  
            "align-items": "center",
            "justify-content": "center",
        },
    )


template_theme1 = "united"
template_theme2 = "solar"
url_theme1 = dbc.themes.UNITED
url_theme2 = dbc.themes.SOLAR

# =========  Layout  =========== #
app.layout = dbc.Container(
    children=[
        dcc.Loading(
            id="loading-1",
            children=[
                dcc.Store(id="database", data={}),
                dcc.Location(id="base-url", refresh=False),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.Img(
                                                                    src="https://voucher.sandvik.com.br/assets/sandvik_coromant-logo-novo-b4cc71950a46b2e9775af000364ff005ef4d0c20515171c3204461d2e48dda21.png",
                                                                    style={
                                                                        "width": "151px",
                                                                        "height": "36px",
                                                                        "margin-botton": "10px",
                                                                    },
                                                                ),
                                                                html.Hr(),
                                                            ],
                                                            sm=12,
                                                            align="center",
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H3(
                                                                    "Tools Analysis"
                                                                )
                                                            ],
                                                            sm=12,
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                ThemeSwitchAIO(
                                                                    aio_id="theme",
                                                                    themes=[
                                                                        url_theme1,
                                                                        url_theme2,
                                                                    ],
                                                                ),
                                                                html.Legend(
                                                                    "Tork tomadas"
                                                                ),
                                                                html.Hr(),
                                                                html.H6(
                                                                    "Escolha o período"
                                                                ),
                                                                dcc.DatePickerRange(
                                                                    id="date-picker-range",
                                                                    end_date=datetime.today(),
                                                                    start_date=datetime.today()
                                                                    - timedelta(
                                                                        days=30
                                                                    ),
                                                                    display_format="YYYY-MM-DD",
                                                                    className="dbc",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                    style={"margin-top": "10px"},
                                                ),
                                            ]
                                        )
                                    ],
                                    style=tab_card,
                                )
                            ],
                            sm=4,
                            lg=2,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    [
                                                        dbc.Tabs(
                                                            [
                                                                dbc.Tab(
                                                                    label="Custo",
                                                                    tab_id="tab-1",
                                                                ),
                                                                dbc.Tab(
                                                                    label="Consumo",
                                                                    tab_id="tab-2",
                                                                ),
                                                            ],
                                                            id="tabs",
                                                            active_tab="tab-1",
                                                        ),
                                                        html.Div(id="card"),
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    style=tab_card,
                                )
                            ],
                            sm=12,
                            lg=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        [
                                                            html.H5("Motivo de troca"),
                                                            dbc.RadioItems(
                                                                id="reasons",
                                                                options=[
                                                                    {
                                                                        "label": "Todos",
                                                                        "value": "",
                                                                    },
                                                                    {
                                                                        "label": "Fim de vida",
                                                                        "value": "Fim de vida",
                                                                    },
                                                                    {
                                                                        "label": "Quebra",
                                                                        "value": "Quebra",
                                                                    },
                                                                    {
                                                                        "label": "Afiação",
                                                                        "value": "Afiação",
                                                                    },
                                                                ],
                                                                value="",
                                                                labelCheckedClassName="text-warning",
                                                                inputCheckedClassName="border border-warning bg-warning",
                                                            ),
                                                            html.Hr(),
                                                            html.H5("Categoria"),
                                                            dbc.RadioItems(
                                                                id="category",
                                                                options=[
                                                                    {
                                                                        "label": "Todos",
                                                                        "value": "",
                                                                    },
                                                                    {
                                                                        "label": "EPI",
                                                                        "value": "EPI",
                                                                    },
                                                                    {
                                                                        "label": "Insertos",
                                                                        "value": "Insertos",
                                                                    },
                                                                    {
                                                                        "label": "Caracol",
                                                                        "value": "Caracol",
                                                                    },
                                                                    {
                                                                        "label": "Abrasivos",
                                                                        "value": "Abrasivos",
                                                                    },
                                                                ],
                                                                value="",
                                                                labelCheckedClassName="text-warning",
                                                                inputCheckedClassName="border border-warning bg-warning",
                                                            ),
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    style=tab_card,
                                )
                            ],
                            sm=12,
                            lg=2,
                        ),
                    ],
                    className="g-2 my-auto",
                    style={"margin-top": "7px"},
                ),
                # Row 2
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    id="graph2",
                                                    className="dbc",
                                                    config=config_graph,
                                                ),
                                                dcc.Graph(
                                                    id="graph3",
                                                    className="dbc",
                                                    config=config_graph,
                                                ),
                                            ]
                                        )
                                    ],
                                    style=tab_card,
                                )
                            ],
                            sm=12,
                            lg=2,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Tabs(
                                                    [
                                                        dbc.Tab(
                                                            label="Operador",
                                                            tab_id="tab-5",
                                                        ),
                                                        dbc.Tab(
                                                            label="Máquina",
                                                            tab_id="tab-6",
                                                        ),
                                                        dbc.Tab(
                                                            label="Ordem",
                                                            tab_id="tab-3",
                                                        ),
                                                        dbc.Tab(
                                                            label="Item",
                                                            tab_id="tab-4",
                                                        ),
                                                    ],
                                                    id="tabs2",
                                                    active_tab="tab-5",
                                                ),
                                                dcc.Graph(
                                                    id="graph1",
                                                    className="dbc",
                                                    config=config_graph,
                                                ),
                                            ]
                                        )
                                    ],
                                    style=tab_card,
                                )
                            ],
                            sm=12,
                            lg=10,
                        ),
                    ],
                    className="g-2 my-auto",
                    style={"margin-top": "7px", "margin-bottom": "7px"},
                ),
            ],
            type="graph",
            fullscreen=True,
        ),
    ],
    fluid=True,
    style={"height": "100vh"},
)


# ======== Callbacks ========== #


@app.callback(
    Output("card", "children"),
    Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    [
        Input("database", "data"),
        Input("tabs", "active_tab"),
        Input("tabs2", "active_tab"),
        Input("reasons", "value"),
        Input("category", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    ],
)
def update_output(data, at, at2, reasons, category, toggle):
    template = template_theme1 if toggle else template_theme2
    if data:
        df_filtered2 = pd.DataFrame(data)
        df_filtered = pd.DataFrame(data)

        # Transformar 'reasons' e 'category' em lista se não forem nulos
        if reasons or reasons != "":
            reasons_list = [reasons]  # Transforma em lista
            df_filtered = df_filtered[df_filtered["Motivo de troca"].isin(reasons_list)]
            df_filtered2 = df_filtered[
                df_filtered["Motivo de troca"].isin(reasons_list)
            ]

        if category:
            category_list = [category]  # Transforma em lista
            df_filtered = df_filtered[df_filtered["Categoria"].isin(category_list)]
            df_filtered2 = df_filtered[df_filtered["Categoria"].isin(category_list)]

        # Agrupar por preço
        groupedPrice = df_filtered.groupby("Nome")["Preço"].sum().reset_index()
        groupedPrice_2 = df_filtered.groupby("Máquina")["Preço"].sum().reset_index()
        groupedPrice_3 = (
            df_filtered.groupby("Código do item")["Preço"].sum().reset_index()
        )
        groupedPrice_4 = (
            df_filtered.groupby("Ordem de produção")["Preço"].sum().reset_index()
        )
        groupedPrice_5 = df_filtered.groupby("Peça")["Preço"].sum().reset_index()

        # Agrupamentos por consumo
        groupedConsumption = (
            df_filtered.groupby("Nome")["Quantidade consumida"].sum().reset_index()
        )
        groupedConsumption_2 = (
            df_filtered.groupby("Máquina")["Quantidade consumida"].sum().reset_index()
        )
        groupedConsumption_3 = (
            df_filtered.groupby("Código do item")["Quantidade consumida"]
            .sum()
            .reset_index()
        )

        # ordenando em ordem ascendente
        groupedPriceAscending_5 = groupedPrice_5.sort_values(by="Preço", ascending=True)
        groupedPriceAscending_4 = groupedPrice_4.sort_values(by="Preço", ascending=True)

        # Removendo as colunas duplicadas
        df_filtered = df_filtered.loc[:, ~df_filtered.columns.duplicated()]

        # top 10 em consumo e valor
        topTenPrice = groupedPrice_3.nlargest(10, ["Preço"])
        topTenConsumption = groupedConsumption_3.nlargest(10, ["Quantidade consumida"])

        # cards
        cards_consumo = [
            criateCard(row["Código do item"], row["Quantidade consumida"], "Quantidade")
            for index, row in topTenConsumption.iterrows()
            if row["Código do item"] and not pd.isna(row["Quantidade consumida"])
        ]

        cards_preco = [
            criateCard(row["Código do item"], row["Preço"], "Preço")
            for index, row in topTenPrice.iterrows()
            if row["Código do item"] and not pd.isna(row["Preço"])
        ]

        cardTopTen1 = html.Div(
            [
                html.Br(),
                html.Br(),
                html.H2("Top 10 itens mais consumidos"),
                html.Br(),
                html.Div(
                    [html.Div(card, style={"margin": "5px"}) for card in cards_consumo],
                    className="card-deck",
                    style={"display": "flex", "flex-wrap": "wrap"},
                ),
            ],
            style={"text-align": "center", "margin": "0 auto"},
        )
        cardTopTen2 = html.Div(
            [
                html.Br(),
                html.Br(),
                html.H2("Top 10 intens em Custo"),
                html.Br(),
                html.Div(
                    [html.Div(card, style={"margin": "5px"}) for card in cards_preco],
                    className="card-deck",
                    style={"display": "flex", "flex-wrap": "wrap"},
                ),
            ],
            style={"text-align": "center", "margin": "0 auto"},
        )

        # Criação dos gráficos

        # consumo  e custo por operador
        fig_operator = make_subplots(specs=[[{"secondary_y": True}]])
        fig_operator.add_trace(
            go.Bar(
                x=groupedConsumption["Nome"],
                y=groupedConsumption["Quantidade consumida"],
                name="Quantidade consumida",
                hovertemplate="Operador: %{x}<br>Quantidade Consumida: %{y} peças<extra></extra>",
            ),
            secondary_y=False,
        )
        fig_operator.add_trace(
            go.Scatter(
                x=groupedPrice["Nome"],
                y=groupedPrice["Preço"],
                mode="lines+markers",
                name="Consumo em Reais",
                hovertemplate="Operador: %{x}<br>Custo: R$%{y:.2f}<extra></extra>",
            ),
            secondary_y=True,
        )
        fig_operator.update_layout(
            showlegend=False,
            title_text="Consumo por Operador",
            template=template,
        )

        # consumo  e custo por máquina
        fig_machine = make_subplots(specs=[[{"secondary_y": True}]])
        fig_machine.add_trace(
            go.Bar(
                x=groupedConsumption_2["Máquina"],
                y=groupedConsumption_2["Quantidade consumida"],
                name="Quantidade consumida",
                hovertemplate="Máquina: %{x}<br>Quantidade: %{y} peças<extra></extra>",
            ),
            secondary_y=False,
        )
        fig_machine.add_trace(
            go.Scatter(
                x=groupedPrice_2["Máquina"],
                y=groupedPrice_2["Preço"],
                mode="lines+markers",
                name="Consumo em Reais",
                hovertemplate="Máquina: %{x}<br>Custo: R$%{y}<extra></extra>",
            ),
            secondary_y=True,
        )
        fig_machine.update_yaxes(title_text="Quantidade Consumida", secondary_y=False)
        fig_machine.update_yaxes(title_text="Preço em Reais", secondary_y=True)
        fig_machine.update_layout(
            title_text="Consumo por máquina", template=template, showlegend=False
        )

        # # custo por ordem de produção
        fig_order = go.Figure()
        fig_order.add_trace(
            go.Bar(
                y=groupedPriceAscending_4["Ordem de produção"],
                x=groupedPriceAscending_4["Preço"],
                name="Consumo em Reais",
                orientation="h",
                hovertemplate="Ordem de Produção: %{y}<br>Custo: R$%{x:.2f}<extra></extra>",
            ),
        )
        fig_order.update_layout(
            title_text="Custo de insumos destinados por ordem de produção",
            template=template,
            showlegend=False,
            xaxis_title="Valor",
            yaxis_title="Ordem",
            autosize=True,
        )

        # # custo por peça
        fig_item = go.Figure()
        fig_item.add_trace(
            go.Bar(
                y=groupedPriceAscending_5["Peça"],
                x=groupedPriceAscending_5["Preço"],
                name="Consumo em Reais",
                orientation="h",
                hovertemplate="Peça: %{y}<br>Custo: R$%{x}<extra></extra>",
            )
        )

        # Atualizar o layout para acomodar as barras horizontais
        fig_item.update_layout(
            title_text="Custo de isnumos destinados por item",
            template=template,  # Certifique-se de que 'template' esteja definido
            showlegend=False,
            xaxis_title="Valor",
            yaxis_title="Peça",
            autosize=True,
        )

        total_gasto = (
            df_filtered2["Preço unitário"] * df_filtered2["Quantidade consumida"]
        ).sum()
        total_consumido = (df_filtered2["Quantidade consumida"]).sum()

        fig2 = go.Figure()
        fig2.add_trace(
            go.Indicator(
                mode="number",
                title={
                    "text": f"<span style='font-size:150%'>Valor Total</span><br><span style='font-size:70%'>Em Reais</span><br>"
                },
                value=total_gasto,
                number={"prefix": "R$"},
            )
        )

        fig2.update_layout(main_config, height=200, template=template)

        fig3 = go.Figure()
        fig3.add_trace(
            go.Indicator(
                mode="number",
                title={
                    "text": f"<span style='font-size:150%'>QNT Total</span><br><span style='font-size:70%'>Peças</span><br>"
                },
                value=total_consumido,
                number={"suffix": "Un"},
            )
        )

        fig3.update_layout(main_config, height=200, template=template)

        if at == "tab-1":
            cardTopTen = cardTopTen2
        elif at == "tab-2":
            cardTopTen = cardTopTen1

        if at2 == "tab-3":
            graph1 = fig_order
        elif at2 == "tab-4":
            graph1 = fig_item
        elif at2 == "tab-5":
            graph1 = fig_operator
        elif at2 == "tab-6":
            graph1 = fig_machine

        return cardTopTen, graph1, fig2, fig3


# Run server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8052, debug=True)
