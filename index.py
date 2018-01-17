import collections
import json
import os
import threading
import urllib.request

import flask


class D2:

    _items_api = 'http://www.dota2.com/jsfeed/heropediadata?feeds=itemdata&v=3326812NSYOcfo4k_6s&l=english'
    _items_local_file_path = 'data/d2_item_list.json'
    _items_cache = None

    _lock = threading.Lock()

    @staticmethod
    def items():
        """
        Returns:
            dict: {name: {'id': 1, ...}}
        """
        with D2._lock:
            if D2._items_cache is None:
                if os.path.exists(D2._items_local_file_path):
                    with open(D2._items_local_file_path, mode='r') as f:
                        items = json.loads(f.read())
                else:
                    items_json = urllib.request.urlopen(
                        D2._items_api).read().decode()
                    with open(D2._items_local_file_path, mode='w') as f:
                        f.write(items_json)
                    items = json.loads(items_json)
                D2._items_cache = D2._filter_items(items['itemdata'])
            return D2._items_cache

    @staticmethod
    def _filter_items(items):
        """Filters unwanted items (which are not standard DotA in game items
        """
        names_to_filter = []
        for name, item in items.items():
            if not (item['attrib'] or item['lore'] and
                    ('greevil' not in item['dname'].lower())):
                names_to_filter.append(name)

        for name in names_to_filter:
            del items[name]

        return items

if __name__ == '__main__':
    # use .format to append <item_name>
    d2_image_url = 'http://cdn.dota2.com/apps/dota2/images/items/{}_lg.png'

    app = flask.Flask("DotA")

    @app.route('/parts/item')
    def _item():
        name = flask.request.args.get('name')
        if not name:
            return '...'
        try:
            items = D2.items()
            item = items[name]
        except KeyError:
            return 'no such item: ' + name

        components = []
        comps = item['components']
        if comps:
            recipe_cost = item['cost']
            for comp_name in comps:
                if not comp_name.startswith('recipe'):
                    comp_cost = items[comp_name]['cost']
                    recipe_cost -= comp_cost
                    components.append(
                        {'img': d2_image_url.format(comp_name),
                         'name': comp_name,
                         'cost': comp_cost,
                         'is_recipe': False})
            if recipe_cost > 0:
                components.append({'img': d2_image_url.format('recipe'),
                                   'name': 'Recipe',
                                   'cost': recipe_cost,
                                   'is_recipe': True})

        return flask.render_template(
            'parts/item.html', lbl=item['dname'], cost=item['cost'],
            desc=item['desc'], notes=item['notes'], attrib=item['attrib'],
            components=components)


    @app.route('/')
    @app.route('/quality')
    def _quality():
        items = collections.defaultdict(list)
        for name, item in D2.items().items():
            items[(item['qual'] or 'component')].append({
                'img': d2_image_url.format(name),
                'lbl': item['dname'],
                'cost': item['cost'],
                'name': name
            })
        for key, val in items.items():
            items[key] = sorted(val, key=lambda i: (i['cost'], i['lbl']))
        return flask.render_template(
            'index.html', items=items, page="quality.html")


    @app.route('/cost')
    def _cost():
        items = collections.defaultdict(list)
        for name, item in D2.items().items():
            item_cost = int(item['cost'])
            item_cost_lbl = item_cost // 1000 * 1000
            item_cost_lbl = str(item_cost_lbl)
            items[item_cost_lbl].append({
                'img': d2_image_url.format(name),
                'lbl': item['dname'],
                'cost': item_cost,
                'name': name
            })
        for key, val in items.items():
            items[key] = sorted(val, key=lambda i: (i['cost'], i['lbl']))
        return flask.render_template(
            'index.html', items=items, page="quality.html")


    app.debug = True
    app.run()
