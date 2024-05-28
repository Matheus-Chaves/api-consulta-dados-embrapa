ROUTE_CONFIG = {
    "base_path": "/processamentos",
    "tags": ["Processamento"],
    "endpoints": {
        "/viniferas": {
            "file_name": "processamento_viniferas.csv",
            "summary": "Processamento de viníferas",
            "description": "Retorna dados sobre uvas viníferas processadas no Rio Grande do Sul.",
        },
        "/uvas-de-mesa": {
            "file_name": "processamento_uvas_de_mesa.csv",
            "summary": "Processamento de uvas de mesa",
            "description": "Retorna dados sobre uvas de mesa processadas no Rio Grande do Sul.",
        },
        "/sem-classificacoes": {
            "file_name": "processamento_sem_classificacao.csv",
            "summary": "Processamento de uvas sem classificação",
            "description": "Retorna dados sobre uvas sem classificação processadas no Rio Grande do Sul.",
        },
        "/americanas-e-hibridas": {
            "file_name": "processamento_americanas_e_hibridas.csv",
            "summary": "Processamento de uvas americanas e híbridas",
            "description": "Retorna dados sobre uvas americanas e híbridas processadas no Rio Grande do Sul.",
        },
    },
}
