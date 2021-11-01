import sqlite3
import json
import math
from sqlite3.dbapi2 import Error

from flask import Flask, request, Response, render_template

app = Flask(__name__)


def open_db():
    db = sqlite3.connect('./transactions.db')
    db.row_factory = sqlite3.Row
    return db


@app.route('/', methods=['GET'])
def transactions():
    return render_template('transactions.html')


@app.route('/categories', methods=['GET'])
def categories():
    return render_template('categories.html')


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    with open_db() as db:
        results = db.execute('SELECT * FROM transactions WHERE date >= "2021-05-01" ORDER BY date ASC')
        return Response(json.dumps([dict(idx) for idx in results.fetchall()]), mimetype='application/json')


@app.route('/api/transactions/<int:id>', methods=['PUT', 'PATCH'])
def update_transaction(id):
    transaction = request.get_json(force=True)
    with open_db() as db:
        db.execute('UPDATE transactions SET category_id = ? WHERE id = ?', (transaction['category_id'], id))
        db.commit()
        return {'success': True}


@app.route('/api/categories', methods=['GET'])
def get_categories():
    with open_db() as db:
        results = db.execute('SELECT * FROM categories')
        return Response(json.dumps([dict(idx) for idx in results.fetchall()]), mimetype='application/json')


@app.route('/api/categories', methods=['POST'])
def create_category():
    category = request.get_json(force=True)
    with open_db() as db:
        db.execute('INSERT INTO categories (name) VALUES (?)', (category.get('name'),))
        db.commit()
        return {'success': True}


@app.route('/api/breakdown', methods=['GET'])
def get_breakdown():
    group_by_first = request.args.get('group_by', 'month').lower()

    with open_db() as db:
        results = db.execute('''
            SELECT
                j.*
            FROM (
                SELECT
                    t.id,
                    t.date,
                    SUBSTR(t.date, 0, 8) as month,
                    t.amount,
                    REPLACE(t.description, '  ', ' ') as description,
                    t.category_id,
                    c.name as category_name,
                    t.source
                FROM transactions t
                INNER JOIN categories c on t.category_id = c.id
                WHERE c.name NOT IN ('Income', 'Payments', 'Savings') AND t.date >= '2021-05'
            ) j
            ORDER BY j.month ASC, j.category_name ASC
        ''')
        # return Response(json.dumps([dict(idx) for idx in results.fetchall()], indent=2), mimetype='application/json')
        transactions = [dict(idx) for idx in results.fetchall()]

        if group_by_first == 'month':
            first_group = 'month'
            second_group = 'category_name'
        elif group_by_first == 'category':
            first_group = 'category_name'
            second_group = 'month'
        else:
            return Response(Error('Invalid group by'))

        aggregated_transactions = {}

        for item in transactions:
            item['description'] = item['description'].replace('  ', ' ', 10).replace('\t', ' ')

            top_group_value = item.get(first_group)
            second_group_value = item.get(second_group)
            if top_group_value in aggregated_transactions.keys():
                if second_group_value in aggregated_transactions[top_group_value].keys():
                    sub_group = aggregated_transactions[top_group_value][second_group_value]
                    sub_group['transactions'].append(item)
                    sub_group['summary']['amount'] += item['amount']
                    sub_group['summary']['total_transactions'] += 1
                    sub_group['summary']['min'] = min(sub_group['summary']['min'], item['amount'])
                    sub_group['summary']['max'] = max(sub_group['summary']['max'], item['amount'])
                    sub_group['summary']['avg'] = round(sub_group['summary']['amount'] / sub_group['summary']['total_transactions'], 2)
                else:
                    aggregated_transactions[top_group_value][second_group_value] = {
                        'summary': {
                            'amount': item['amount'],
                            'total_transactions': 1,
                            'min': item['amount'],
                            'max': item['amount'],
                            'avg': item['amount']
                        },
                        'transactions': [item]
                    }
            else:
                aggregated_transactions[top_group_value] = {}
                aggregated_transactions[top_group_value][second_group_value] = {
                    'summary': {
                        'amount': item['amount'],
                        'total_transactions': 1,
                        'min': item['amount'],
                        'max': item['amount'],
                        'avg': item['amount']
                    },
                    'transactions': [item]
                }

        
        return Response(json.dumps(aggregated_transactions, indent=2), mimetype='application/json')
