ROUTE_CONFIG = {
    "base_path": "/importacoes",
    "tags": ["Importação"],
    "endpoints": {
        "/espumantes": {
            "file_name": "importacao_espumantes.csv",
            "summary": "Importações de espumantes.",
            "description": "Retorna os dados de importações de vinhos de mesa."
        },
        "/sucos-de-uva": {
            "file_name": "importacao_suco_de_uva.csv",
            "summary": "Importações de sucos de uva.",
            "description": "Retorna os dados de importações de sucos de uva."
        },
        "/uvas-frescas": {
            "file_name": "importacao_uvas_frescas.csv",
            "summary": "Importações de uvas frescas",
            "description": "Retorna os dados de importações de uvas frescas."
        },
        "/uvas-passas": {
            "file_name": "importacao_uvas_passas.csv",
            "summary": "Importações de uvas passas",
            "description": "Retorna os dados de importações de uvas passas."
        },
        "/vinhos-de-mesa": {
            "file_name": "importacao_vinhos_de_mesa.csv",
            "summary": "Importações de vinhos de mesa",
            "description": "Retorna os dados de importações de vinhos de mesa."
        },
    }
}