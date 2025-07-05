def add_prefixed_metrics(target_dict, source_dict, prefix):
    for key, value in source_dict.items():
        target_dict[f"{prefix}_{key}"] = value
