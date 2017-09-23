from wsgiref.simple_server import make_server
from string import Template
import json
import re

with open('templates/index.html', 'r') as html:
    template = Template(html.read())


def regex_app(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    if method == "GET":
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)

        context = {
            "name": "Python Regex",
        }

        return [template.substitute(context).encode('utf-8')]

    if method == "POST":

        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        data = json.loads(environ.get('wsgi.input').read(request_body_size))
        regex = eval("r\"" + data.get('regex', '') + "\"")
        test = data.get('test', '')
        sub = eval("r\"" + data.get('replace', '') + "\"")

        matches = re.findall(regex, test, re.MULTILINE)
        replaced = re.sub(regex, sub, test, 0, re.MULTILINE)

        status = '200 OK'
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        result = {
            "matches": matches,
            "replaced": replaced,
        }
        return [json.dumps(result).encode('utf-8')]


with make_server('', 8000, regex_app) as httpd:
    print("Serving HTTP on port 8000...")
    httpd.serve_forever()
