from flask import Flask, request, jsonify
import unittest

app = Flask(__name__)
todo_list = []

# ----------- Flask Routes (Web App) -----------

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todo_list), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if 'task' not in data:
        return jsonify({'error': 'Task is required'}), 400
    todo_list.append({'task': data['task'], 'done': False})
    return jsonify({'message': 'Task added'}), 201

@app.route('/todos/<int:index>', methods=['PUT'])
def mark_done(index):
    if index < 0 or index >= len(todo_list):
        return jsonify({'error': 'Invalid index'}), 404
    todo_list[index]['done'] = True
    return jsonify({'message': 'Task marked as done'}), 200

@app.route('/todos', methods=['DELETE'])
def clear_todos():
    todo_list.clear()
    return jsonify({'message': 'All tasks cleared'}), 200

# ----------- Unit Tests -----------
class ToDoTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        todo_list.clear()

    def test_add_todo(self):
        response = self.client.post('/todos', json={'task': 'Test Task'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(todo_list[0]['task'], 'Test Task')

    def test_get_todos(self):
        self.client.post('/todos', json={'task': 'Read Book'})
        response = self.client.get('/todos')
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['task'], 'Read Book')

    def test_mark_done(self):
        self.client.post('/todos', json={'task': 'Write Code'})
        response = self.client.put('/todos/0')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(todo_list[0]['done'])

    def test_clear_todos(self):
        self.client.post('/todos', json={'task': 'Clear Test'})
        response = self.client.delete('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(todo_list), 0)

    def test_add_todo_missing_task(self):
        response = self.client.post('/todos', json={})
        self.assertEqual(response.status_code, 400)

    def test_invalid_index(self):
        response = self.client.put('/todos/99')
        self.assertEqual(response.status_code, 404)

# ----------- Main Entry Point -----------

if __name__ == '__main__':
    import sys
    if 'test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        app.run(debug=True)
