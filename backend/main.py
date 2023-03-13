from flask import Flask, jsonify, request 
from flask_cors import CORS
import uuid

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})


Statuses = [
    {
    'id' : uuid.uuid4().hex,
    'name' : 'first',
    'type' : 'initial',
    },
    {
    'id' : uuid.uuid4().hex,
    'name' : 'second',
    'type' : 'orphan',
    },
    {
    'id' : uuid.uuid4().hex,
    'name' : 'last',
    'type' : 'final',
    }
]

Transitions = [
    {
    'id' : uuid.uuid4().hex,
    'name' : 'trans1',
    'from' : 'first',
    'to' : 'last',
    }
]


@app.route('/', methods=['GET', 'POST'])
def all_status():
    response_object = {'status':'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data.get('type') != '':
            for s in Statuses:
                if s['name'] == post_data.get('name'):
                    # response_object['status'] = 'error'
                    response_object['message1'] = 'Status with name already exists!'
                    return jsonify(response_object)
                if s['type'] == post_data.get('type'):
                    if s['type'] == 'initial':
                        # response_object['status'] = 'error'
                        response_object['message1'] = 'There is another initial!'
                        return jsonify(response_object)
            if post_data.get('type') != 'initial':
                if post_data.get('type') != 'orphan':
                    if post_data.get('type') != 'final':
                        # response_object['status'] = 'error'
                        response_object['message1'] = 'Inccorect type'
                        return jsonify(response_object)
            Statuses.append({
            'id' : uuid.uuid4().hex,
            'name': post_data.get('name'),
            'type': post_data.get('type')})
            response_object['message'] = 'Status Added!'
        else:
            name = post_data.get('name')
            to = post_data.get('to')
            fromm = post_data.get('from')
            if any(t['name'] == name for t in Transitions):
                response_object['message1'] = 'Transition with name already exists!'
                return response_object
            if any(s['name'] == to for s in Statuses):
                if any(s['name'] == fromm for s in Statuses):
                    Transitions.append({
                    'id' : uuid.uuid4().hex,
                    'name': name,
                    'from': post_data.get('from'),
                    'to': post_data.get('to')})
                    response_object['message'] = 'Transition Added!'
                    return response_object
            else:
                response_object['message1'] = 'There is no Status that match the "to" value or the "from" value'
    else:
        response_object['Statuses'] = Statuses
        response_object['Transitions'] = Transitions
    return jsonify(response_object)



@app.route('/clear', methods=['POST'])
def clear_database():
    response_object = {'status':'success'}
    Statuses.clear()
    Transitions.clear()
    response_object['message'] = 'Configuration cleared'
    return jsonify(response_object)



# PUT and DELETE route handler
@app.route('/<status_id>', methods=['PUT','DELETE'])
def single_status(status_id):
    response_object = {'status':'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        print(post_data)
        if post_data.get('from') == '':
            for s in Statuses:           
                if s['name'] == post_data.get('name'):
                    response_object['message1'] = 'Duplicated status name!'
                    return jsonify(response_object)
            for s in Statuses: 
                if s['id'] == status_id:
                    s['name'] = post_data.get('name')
                    s['type'] = post_data.get('type')
            response_object['message'] = 'Status updated!'
        else:             
            for t in Transitions:
                if t['name'] == post_data.get('name'):
                    response_object['message1'] = 'Duplicated transition name!'
                    return jsonify(response_object)
            if t['id'] == status_id:
                    t['name'] = post_data.get('name')
                    t['from'] = post_data.get('from')
                    t['to'] = post_data.get('to')
            response_object['message'] = 'Transition updated!'
    if request.method == 'DELETE':
        remove_status(status_id)
        remove_transition(status_id)
        response_object['message'] = 'Status Removed!'
    return jsonify(response_object)


        

def remove_status(status_id):
    for status in Statuses:
        if status['id'] == status_id:
            if Transitions:
                for t in Transitions:
                    if t['from'] == status['name']:
                        remove_transition(t['id'])
                    if t['to'] == status['name']:
                        remove_transition(t['id']) 
            Statuses.remove(status)
            return True
    return False


def remove_transition(transition_id):
    for transition in Transitions:
        if transition['id'] == transition_id:
            Transitions.remove(transition)
            return True
    for transition in Transitions:
        if transition['from'] not in [status['name'] for status in Statuses] or transition['to'] not in [status['name'] for status in Statuses]:
            Transitions.remove(transition)
    return False




if __name__ == "__main__":
    app.run(debug=True)
