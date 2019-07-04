# -*- coding: utf-8 -*-
import shutil
import os
from glob import glob
from fabric.api import cd, env, local, run, task, put
from fabric.contrib import project
from jinja2 import Template
from glob import glob


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


@task(alias='ass')
def assets():
    for tsx in glob('src/components/**/*.tsx', recursive=True):
        print(tsx)
    for tsx in glob('src/pages/**/*.tsx', recursive=True):
        print(tsx)


@task(alias='mod')
def models():
    '''models 构建'''
    models = glob('src/models/*.tsx', recursive=True)
    export = []

    for model in models:
        model = os.path.basename(model).replace('.tsx', '')
        if 'index' not in model:
            export.append(model)

    imports = ["import {} from './{}'".format(x, x) for x in export]
    tsx = '\n'.join(imports) + '\n'
    tsx += '\nexport default [' + ', '.join(export) + ']'

    with open('src/models/index.tsx', 'w') as fp:
        fp.write(tsx)

    print(tsx)


# @task(alias='conv')
# def convert():
#     ''' 转换小程序为Taro项目'''
#     local('taro convert')
#     renane()
#     replace()

@task(alias='ren')
def renane():
    '''.js 改名 .tsx'''
    js = glob('src/**/*.js', recursive=True)

    for x in js:
        shutil.move(x,  x.replace('.js', '.tsx'))
        print(x)
        # print(x, x.replace('.js', '.tsx'))

@task()
def fix():
    '''.js 改名 .tsx'''
    tsx = glob('src/components/**/*.tsx', recursive=True)
    
    for x in tsx:
        shutil.copy(x, '{}.bak'.format(x))
        
        z = open(x).read()
        z = z.replace('"', "'")
        
        with open(x, 'w') as fp:
            fp.write(z)
        
        print(x)
        # y = 'src/pages/{}.tsx'.format(x.split('/')[2])

@task
def m():
    '''.js 改名 .tsx'''
    js = glob('src/**/model.tsx', recursive=True)

    for x in js:
        # shutil.move(x,  x.replace('.js', '.tsx'))
        y = 'src/models/{}.tsx'.format(x.split('/')[2])
        print(x)
        print(y)
        shutil.copy(x, y)
        # print(x, x.replace('.js', '.tsx'))


@task
def s():
    '''.js 改名 .tsx'''
    js = glob('src/**/service.tsx', recursive=True)

    for x in js:
        # shutil.move(x,  x.replace('.js', '.tsx'))
        y = 'src/services/{}.tsx'.format(x.split('/')[2])
        print(x)
        print(y)
        shutil.copy(x, y)
        # print(x, x.replace('.js', '.tsx'))


@task(alias='rep')
def replace(environ='dev'):
    '''替换文件内 setData => setState'''
    tsx = glob('src/**/*.tsx', recursive=True)

    for x in tsx:
        com = os.path.basename(x).split('.')[0].capitalize()
        txt = ''

        with open(x, 'r') as fs:
            txt = fs.read()
            txt = txt.replace('_C', com)
            txt = txt.replace('this.setData', 'this.setState')
            txt = txt.replace('this.data', 'this.state')
            txt = txt.replace('that.data.', 'this.state.')
            txt = txt.replace('page.data.', 'this.state.')
            txt = txt.replace('let page = this', '')
            txt = txt.replace('let that = this', '')
            txt = txt.replace(
                'componentWillMount = options => {', 'componentWillMount = () => {\n\tconst options = this.$router.params')
            txt = txt.replace(
                'componentWillMount = e => {', 'componentWillMount = () => {\n\tconst e = this.$router.params')
            txt = txt.replace('config = {', 'config: Config = {')
            txt = txt.replace('Taro.navigateBack(1)',
                              'Taro.navigateBack({ delta: 1 })')
            txt = txt.replace("import withWeapp from '@tarojs/with-weapp'", '')
            txt = txt.replace(
                "extends Taro.Component {", "extends Component {")
            txt = txt.replace("import Taro from '@tarojs/taro'",
                              "import Taro, { Component, Config } from '@tarojs/taro'")

        with open(x, 'w') as fp:
            fp.write(txt)

        print(x, com)


@task
def dep():
    '''安装依赖'''
    local("yarn")


@task
def dev():
    '''开发项目'''
    local("""sed -i '' 's/"urlCheck": true/"urlCheck": false/g'  project.config.json""")
    local("""sed -i '' 's/debug: false/debug: true/g'  src/app.tsx""")
    local("yarn dev:weapp")


@task
def pre():
    '''打包项目'''
    local("""sed -i '' 's/"urlCheck": false,/"urlCheck": true,/g'  project.config.json""")
    local("""sed -i '' 's/debug: true,/debug: false,/g'  src/app.tsx""")
    local("yarn build:weapp")


@task
def cls():
    '''清理函数'''
    # local("find ./src -name '*.js' -exec rm -f {} +")
    # local("rm -rf node_modules")
    local("rm -rf __pycache__")
    local("rm -rf dist")


@task(alias='g')
def gen(name='demo'):
    '''编译项目'''
    path = 'src/pages/{}'.format(name)

    if not os.path.isdir(path):
        os.mkdir(path)

    for x in glob('.template/pages/*'):
        template = Template(open(x).read())
        content = template.render(name=name)
        filename = 'src/pages/{}/{}'.format(name, os.path.basename(x))

        with open(filename, 'w') as fp:
            fp.write(content)

        print(filename)


@task
def pak():
    '''文件打包'''
    local('tar zcfv ./dist.tgz '
          '--exclude=.git '
          '--exclude=.tox '
          '--exclude=.env '
          '--exclude=.idea '
          '--exclude=*.tgz '
          '--exclude=*.pyc '
          '--exclude=.vagrant '
          '--exclude=assets/media/* '
          '--exclude=assets/static/* '
          '--exclude=runtime/* '
          '--exclude=.DS_Store '
          '--exclude=.phpintel '
          '--exclude=.template '
          '--exclude=db.sqlite3 '
          '--exclude=Vagrantfile .')
