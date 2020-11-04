"""A simple flask app to return random Real Estate properties."""


from math import ceil

from flask import Flask, request, jsonify, render_template, Markup
from faker import Faker
import markdown


app = Flask(__name__)


def random_cost(faker, min_order=5, max_order=6):
    """Return a random money amount in the correct order of magintude."""
    order = faker.random_int(min_order, max_order)
    return float(''.join([
        str(faker.random_number(order)),
        '.',
        str(faker.random_number(2))
    ]))


def random_property(faker):
    """
    Return a dict which represets a property.

    The order of these is important to keep the random seed the same. When
    adding new fields the data will change.
    """
    return dict([
        ('property_id', faker.sha1()),
        ('street_address', faker.street_address()),
        ('city', faker.city()),
        ('country', faker.country()),
        ('post_code', faker.postcode()),
        ('latitude', float(faker.latitude())),
        ('longitude', float(faker.longitude())),
        ('bedrooms', faker.random_int(min=1, max=5)),
        ('cost', random_cost(faker)),
        ('deposit', random_cost(faker, 2, 4)),
    ])


@app.route('/')
def home():
    """Render the README.md as html."""
    with open('README.md') as f:
        content = markdown.markdown(
            f.read(),
            extensions=['markdown.extensions.tables']
        )
    content = content.replace('<table>', '<table class="table">')
    return render_template('index.html', content=Markup(content))


@app.route('/api/')
def api():
    """The only route. Return predictable but random Real Estate properties."""
    per_page = request.args.get('per_page', 10, int)
    page = request.args.get('page', 0, int)
    total = request.args.get('total', per_page * 2, int)
    seed = request.args.get('seed', 1337405335, int)
    skipped = per_page * page

    Faker.seed(seed)
    faker = Faker()

    properties = []
    for x in range(total):
        prop = random_property(faker)
        if skipped <= x < min(skipped + per_page, total):
            properties.append(prop)

    return jsonify({
        'properties': properties,
        'per_page': per_page,
        'page': page,
        'total': total,
        'total_pages': ceil(total / per_page),
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
