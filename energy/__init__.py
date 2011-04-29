from pyramid.config import Configurator
from energy.resources import Root

def main(global_config, **settings):
     
    config = Configurator(root_factory=Root, \
                          settings={'mako.directories':['energy:templates']})

    config.add_route('root', '', view='energy.views.root_view')
    
    config.add_route('data', '/data/{month}/{day}/{year}/{location}', 
                    view='energy.views.dateview',
                    renderer = 'energy:templates/layout.mako')

    config.add_route('test', '/test',
                     view='energy.views.test',
                     renderer='energy:templates/test.mako')

    config.add_static_view('static', 'energy:static')
    return config.make_wsgi_app()
