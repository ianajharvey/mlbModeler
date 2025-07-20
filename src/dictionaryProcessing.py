def add_prefixed_metrics(target_dict, source_dict, prefix):
    for key, value in source_dict.items():
        target_dict[f"{prefix}_{key}"] = value


def head_to_head_stats(dict_one, dict_two):
    matchup_dict = {}
    for key in dict_one:
        home_stat = dict_one.get(key, 0)
        away_stat = dict_two.get(key, 0)
        matchup_dict[key] = home_stat - away_stat

    return matchup_dict
