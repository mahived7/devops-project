from flask import Flask, request, jsonify, render_template_string
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'app_request_count_total',
    'Total number of requests',
    ['method', 'endpoint']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

# In-memory task store
tasks = []
task_id_counter = [1]

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevOps Task Manager</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: sans-serif; background: #f5f5f5; display: flex; justify-content: center; padding: 2rem 1rem; }
    .container { width: 100%; max-width: 520px; }
    h1 { font-size: 22px; font-weight: 600; margin-bottom: 1.5rem; color: #1a1a1a; }
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 1.25rem; }
    .stat { background: white; border-radius: 10px; padding: 12px; text-align: center; border: 1px solid #e5e5e5; }
    .stat .num { font-size: 22px; font-weight: 600; color: #1a1a1a; }
    .stat .lbl { font-size: 12px; color: #888; margin-top: 2px; }
    form.add-form { display: flex; gap: 8px; margin-bottom: 1.25rem; }
    form.add-form input { flex: 1; padding: 9px 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; }
    form.add-form button { padding: 9px 18px; background: #534AB7; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; }
    form.add-form button:hover { background: #3C3489; }
    .task { display: flex; align-items: center; gap: 10px; padding: 11px 14px; background: white; border: 1px solid #e5e5e5; border-radius: 10px; margin-bottom: 8px; }
    .task.done { background: #f9f9f9; }
    .task.done .task-text { text-decoration: line-through; color: #aaa; }
    .task-text { flex: 1; font-size: 14px; color: #1a1a1a; }
    .btn-sm { padding: 5px 10px; font-size: 12px; border-radius: 6px; border: 1px solid #ddd; cursor: pointer; background: white; }
    .btn-done { border-color: #0F6E56; color: #0F6E56; }
    .btn-done:hover { background: #E1F5EE; }
    .btn-undo { border-color: #888; color: #888; }
    .btn-del { border-color: #993C1D; color: #993C1D; }
    .btn-del:hover { background: #FAECE7; }
    .empty { text-align: center; color: #aaa; font-size: 14px; padding: 2rem 0; }
  </style>
</head>
<body>
<div class="container">
  <h1>&#10003; DevOps Task Manager</h1>

  <div class="stats">
    <div class="stat"><div class="num">{{ tasks|length }}</div><div class="lbl">Total</div></div>
    <div class="stat"><div class="num">{{ tasks|selectattr('done')|list|length }}</div><div class="lbl">Done</div></div>
    <div class="stat"><div class="num">{{ tasks|rejectattr('done')|list|length }}</div><div class="lbl">Pending</div></div>
  </div>

  <form class="add-form" method="POST" action="/add">
    <input name="title" placeholder="Add a new task..." required autocomplete="off" />
    <button type="submit">+ Add</button>
  </form>

  {% if tasks %}
    {% for task in tasks %}
    <div class="task {{ 'done' if task.done }}">
      <span class="task-text">{{ task.title }}</span>
      <form method="POST" action="/complete/{{ task.id }}" style="display:inline">
        <button class="btn-sm {{ 'btn-undo' if task.done else 'btn-done' }}" type="submit">
          {{ 'Undo' if task.done else 'Done' }}
        </button>
      </form>
      <form method="POST" action="/delete/{{ task.id }}" style="display:inline">
        <button class="btn-sm btn-del" type="submit">Delete</button>
      </form>
    </div>
    {% endfor %}
  {% else %}
    <p class="empty">No tasks yet. Add one above!</p>
  {% endif %}
</div>
</body>
</html>
'''

def track(endpoint, method="GET"):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

@app.route('/')
def index():
    start = time.time()
    track('/', 'GET')
    resp = render_template_string(HTML, tasks=tasks)
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    return resp

@app.route('/add', methods=['POST'])
def add_task():
    track('/add', 'POST')
    title = request.form.get('title', '').strip()
    if title:
        tasks.append({'id': task_id_counter[0], 'title': title, 'done': False})
        task_id_counter[0] += 1
    return index()

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    track('/complete', 'POST')
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    return index()

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    track('/delete', 'POST')
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return index()

@app.route('/health')
def health():
    track('/health', 'GET')
    return jsonify({"status": "healthy", "tasks_count": len(tasks)})

@app.route('/metrics')
def metrics():
    track('/metrics', 'GET')
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)