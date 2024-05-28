ROUTE_CONFIG = {
    "base_path": "/producoes",
    "tags": ["Produção"],
    "endpoints": {
        "/": {
            "file_name": "producao_dados.csv",
            "summary": "Dados de produção da vitivinicultura.",
            "description": "Retorna os dados relacionados à produção de vinhos,"
            " sucos e derivados do Rio Grande do Sul.",
        }
    },
}
