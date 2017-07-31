"""Orange Theme for PytSite Blog Application
"""
from pytsite import package_info, tpl, widget, assetman, plugman, router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Check for Blog application presence
if package_info.name('app') != 'blog':
    raise RuntimeError('This theme is able to work only with PytSite Blog application. '
                       'See https://github.com/pytsite/blog for details.')

# Assetman tasks
assetman.t_js('**')
assetman.t_copy_static('**')
assetman.t_less('**')

# Preload permanent assets
assetman.preload('twitter-bootstrap', True)
assetman.preload('font-awesome', True)
assetman.preload('css/common.css', True)
assetman.preload('js/index.js', True)

# Register template globals
tpl.register_global('language_nav',
                    lambda: widget.select.LanguageNav('language-nav', css='navbar-right', dropdown=True))

if plugman.is_installed(['content', 'section', 'article', 'page']):
    from plugins import content, section
    from . import controllers

    router.handle(controllers.Home(), '/', 'home')

    # These two routes needed by 'article' plugin as final point while processing request
    router.handle(controllers.ContentEntityIndex(), name='content_entity_index')
    router.handle(controllers.ContentEntityView(), name='content_entity_view')

    # "Article index by section" route
    router.handle('content@index', '/section/<term_alias>', 'article_index_by_section', {
        'model': 'article',
        'term_field': 'section',
    })

    # "Article index by tag" route
    router.handle('content@index', '/tag/<term_alias>', 'article_index_by_tag', {
        'model': 'article',
        'term_field': 'tags',
    })

    # "Article index by author" route
    router.handle('content@index', '/author/<author>', 'article_index_by_author', {
        'model': 'article',
    })

    # Template globals
    tpl.register_global('content_pages', lambda: list(content.find('page').get()))
    tpl.register_global('content_sections', lambda: list(section.get()))
