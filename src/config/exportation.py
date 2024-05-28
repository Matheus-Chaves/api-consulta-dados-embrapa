ROUTE_CONFIG = {
    "base_path": "/exportacoes",
    "tags": ["Exportação"],
    "endpoints": {
        "/espumantes": {
            "file_name": "exportacao_espumantes.csv",
            "summary": "Exportações de espumantes.",
            "description": "Retorna os dados de exportações de vinhos de mesa.",
        },
        "/sucos-de-uva": {
            "file_name": "exportacao_suco_de_uva.csv",
            "summary": "Exportações de sucos de uva.",
            "description": "Retorna os dados de exportações de sucos de uva.",
        },
        "/uvas-frescas": {
            "file_name": "exportacao_uvas_frescas.csv",
            "summary": "Exportações de uvas frescas",
            "description": "Retorna os dados de exportações de uvas frescas.",
        },
        "/vinhos-de-mesa": {
            "file_name": "exportacao_vinhos_de_mesa.csv",
            "summary": "Exportações de vinhos de mesa",
            "description": "Retorna os dados de exportações de vinhos de mesa.",
        },
    },
}
