def divide_list_by_size(lst, size=3):
    return [lst[i:i + size] for i in range(0, len(lst), size)]
