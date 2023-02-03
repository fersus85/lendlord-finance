from jinja2 import Template
import datetime

day = datetime.date.today().strftime('%d')
days = [i for i in range(1, 4)]

link = """
    {% for d in days %}
    {% if d == day %}
    <li><span class="active">{{ d }}</span></li>
    {% else %}
    <li>{{ d }}</li>
    {% endif%}
    {% endfor %}
    """
tm = Template(link)
msg = tm.render(days=days, day=int(day))
print(msg)
print(type(day))
