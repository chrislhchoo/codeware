from jinja2 import Environment,PackageLoader,FileSystemLoader

from datetime import datetime

if __name__ == '__main__':
    env = Environment(loader=FileSystemLoader(r'D:\py\jinja_template\templates', 'utf-8'))
    template = env.get_template('hello.html')
    print(template.render(name='Chris'))
