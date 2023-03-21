APP_CONFIG = {
    "sub_dyn_inventory": {
        "topic": "SOW/INVENTORY",
        "timeout": 300,
    },
    "prometheus": {
        "port": 5790,
    },
    "sub_dyn_alog_prices": {
        "topic": "SOW/PRICES",
        "timeout": 100,
    },
}


ENV_CONFIG = {
    "prod": {
        "sub_dyn_inventory": {
            "timeout": 700,
        }
    },
    "qa": {
        "sub_dyn_inventory": {
            "timeout": 1200,
        }
    },
    "local": {
        "sub_dyn_inventory": {
            "timeout": 900,
        }
    },
}
