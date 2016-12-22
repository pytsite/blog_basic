"""PytSite Blog Default Theme.
"""
from pytsite import tpl, widget, browser, assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


browser.include('bootstrap', True)
assetman.add('css/common.css', True)
assetman.add('js/common.js', True)

tpl.register_global('theme_blog_default', {
    'language_nav': lambda: widget.select.LanguageNav('language-nav', css='navbar-right', dropdown=True),
})

