def update_without_overwrite(original_dict, new_dict):
    for key, value in new_dict.items():
        if key not in original_dict:
            original_dict[key] = value
        else:
            raise ValueError(f"Key {key} already exists in the original dictionary")