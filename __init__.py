"""PytSite Blog Default Theme
"""
from pytsite import tpl, widget, assetman, plugman, router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Assetman tasks
assetman.t_js('**')
assetman.t_copy_static('**')
assetman.t_less('**')

# Assets preload
assetman.preload('twitter-bootstrap', True)
assetman.preload('font-awesome', True)
assetman.preload('css/common.css', True)
assetman.preload('js/index.js', True)

# Template globals
tpl.register_global('language_nav',
                    lambda: widget.select.LanguageNav('language-nav', css='navbar-right', dropdown=True))

if plugman.is_installed('content'):
    from plugins import content

    if plugman.is_installed('article'):
        # 'Article index by section' route
        router.handle('/section/<term_alias>', 'content@index', 'article_index_by_section', {
            'model': 'article',
            'term_field': 'section',
        })

        # 'Article index' by tag route
        router.handle('/tag/<term_alias>', 'content@index', 'article_index_by_tag', {
            'model': 'article',
            'term_field': 'tags',
        })

        # 'Article index by author' route
        router.handle('/author/<author>', 'content@index', 'article_index_by_author', {
            'model': 'article',
        })

    if plugman.is_installed('page'):
        # Tpl globals
        tpl.register_global('content_pages', lambda: list(content.find('page').get()))

    if plugman.is_installed('section'):
        from plugins import section

        # Tpl globals
        tpl.register_global('content_sections', lambda: list(section.get()))
