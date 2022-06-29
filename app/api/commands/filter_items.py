
def filter_items(data):
    items = []
    for item in data:
        i = {}
        for key, value in item.items():
            if key == 'amount':
                i['amount'] = abs(value)
            if key == 'description':
                i['description'] = value
            if key == 'qty':
                i['quantity'] = value
        items.append(i)

    return items
