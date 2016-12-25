"""PytSite Blog Default Theme.
"""
from pytsite import tpl, widget, browser, assetman, lang, events, theme

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

default_colors = ['#ffffff', '#e6e6e6', '#ff7148', '#263248', '#333333']


def on_assetman_build_before():
    s = theme.get_theme_settings(__name__)

    for n in range(1, 6):
        k = 'color{}'.format(n)
        assetman.register_global(k, s.get(k, default_colors[n - 1]), True)


def get_settings_widgets():
    r = list()

    for n in range(1, 6):
        r.append(widget.select.ColorPicker(
            uid='color{}'.format(n),
            label=lang.t(__name__ + '@color_{}'.format(n)),
            default=default_colors[n - 1],
            h_size='col-xs-12 col-sm-2 col-lg-1',
        ))

    return r


browser.include('bootstrap', True)
assetman.add('css/common.css', True)
assetman.add('js/common.js', True)

# Event listeners
events.listen('pytsite.assetman.build.before', on_assetman_build_before)

tpl.register_global('theme_blog_default', {
    'language_nav': lambda: widget.select.LanguageNav('language-nav', css='navbar-right', dropdown=True),
})
