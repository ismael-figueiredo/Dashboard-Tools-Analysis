import os
import dash
import requests
from app import *
import pandas as pd
from database import *
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

load_figure_template(["minty", "pulse", "united"])
load_dotenv()

template = "united"
url = os.environ.get("url")
username = os.environ.get("username")
password = os.environ.get("password")
config = (username, password)


@app.callback(
    Output("database", "data"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
        Input("base-url", "pathname"),
    ],
)
def updateLocalStorage(start_date, end_date, pathname):
    if start_date is None or end_date is None:
        raise dash.exceptions.PreventUpdate
    if pathname != "":
        # Formata as datas para o formato correto
        start_date_formatted = pd.to_datetime(start_date).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_date_formatted = pd.to_datetime(end_date).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Atualiza a URL com as novas datas formatadas e filtra pelo periodo de tempo direto nos parametros da rota
        filteredDate = f"?$filter=TimeStamp ge {start_date_formatted} and TimeStamp le {end_date_formatted}"
        fullUrl = url + filteredDate
        response = requests.get(fullUrl, auth=config)
        data = response.json().get("value", [])
        if not data:
            print("Nenhum dado encontrado ou erro na resposta.")
            raise dash.exceptions.PreventUpdate

        df = pd.DataFrame(data)

        # As colunas originais do DataFrame que você deseja manter
        selectedColumns = [
            "CostAllocation0",
            "CaLevel0Name",
            "CostAllocation1",
            "CostAllocation2",
            "CostAllocation3",
            "CostAllocation4",
            "TransactionType",
            "PartNumber",
            "ProductName",
            "ItemTypeId",
            "UserFullName",
            "ItemTypeText",
            "Quantity",
            "Category",
            "StockLocationRule",
            "SerialNumber",
            "VendorName",
            "ManufacturerName",
            "Price",
            "Currency",
            "UnitPrice",
            "UnitOfMeasure",
            "ConsumedQuantity",
            "CreatedOn",
        ]

        # Filtra o DataFrame para manter apenas as colunas selecionadas
        df_filtered = df[selectedColumns]
        df_filtered = df_filtered[df_filtered["Price"].fillna(0) > 0]

        # Filtra para ter apenas itens com quantidade consumida maior ou igual a 0
        df_filtered = df_filtered[df_filtered["ConsumedQuantity"].fillna(0) >= 0]

        # Renomeia as colunas do DataFrame filtrado para português
        newTitles = [
            "Nome",
            "Função",
            "Máquina",
            "Peça",
            "Ordem de produção",
            "Motivo de troca",
            "Tipo de Transação",
            "Código do item",
            "Descrição do item",
            "Tipo de item",
            "Usuário",
            "Tipo de item",
            "Quantidade",
            "Categoria",
            "Estado",
            "Número de série",
            "Fornecedor",
            "Marca",
            "Preço",
            "Moeda",
            "Preço unitário",
            "Unidade de medida",
            "Quantidade consumida",
            "Criado em",
        ]

        df_filtered.columns = newTitles

        # Converter as colunas para numérico
        df_filtered["Preço"] = pd.to_numeric(df_filtered["Preço"], errors="coerce")
        df_filtered["Preço unitário"] = pd.to_numeric(
            df_filtered["Preço unitário"], errors="coerce"
        )
        df_filtered["Unidade de medida"] = pd.to_numeric(
            df_filtered["Unidade de medida"], errors="coerce"
        )
        df_filtered["Quantidade consumida"] = pd.to_numeric(
            df_filtered["Quantidade consumida"], errors="coerce"
        )
        # Removendo as colunas duplicadas
        df_filtered = df_filtered.loc[:, ~df_filtered.columns.duplicated()]

        database = df_filtered.to_dict("records")

        return database
