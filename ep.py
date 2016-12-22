"""PytSite Blog Default Theme Endpoints.
"""
from datetime import datetime, timedelta
from pytsite import content, tpl, odm, lang, settings, comments, auth, plugman
from app import model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def home(args: dict, inp: dict) -> str:
    """Home.
    """
    exclude_ids = []

    latest = _get_articles(exclude_ids, 3)

    sections = list(content.get_sections())
    latest_by_section = {}
    for sec in sections:
        latest_by_section[sec.alias] = _get_articles(exclude_ids, 4, section=sec)

    args.update({
        'sections': sections,
        'latest_articles': latest,
        'latest_by_section': latest_by_section,
        'sidebar': _get_sidebar(exclude_ids),
    })

    return tpl.render('$theme@home', args)


def content_article_index(args: dict, inp: dict) -> str:
    """Index of articles.
    """
    args.update(content.paginate(args['finder']))

    exclude_ids = [e.id for e in args.get('entities')]
    args.update({
        'sidebar': _get_sidebar(exclude_ids),
    })

    if 'author' in args and args['author']:
        args['author_widget'] = auth.widget.Profile('user-profile', user=args['author'])

    return tpl.render('$theme@content/index', args)


def content_article_view(args: dict, inp: dict) -> str:
    """Single article view.
    """
    e = args['entity']
    exclude_ids = [e.id]

    args.update({
        'related': _get_articles(exclude_ids, 3, e.section, 'views_count') if e.model == 'article' else [],
        'entity_tags': content.widget.EntityTagCloud('entity-tag-cloud', entity=args['entity']),
        'sidebar': _get_sidebar(exclude_ids),
    })

    if plugman.is_installed('addthis'):
        from plugins import addthis
        args.update({
            'share_widget': addthis.widget.AddThis('add-this-share') if settings.get('addthis.pub_id') else '',
        })

    if plugman.is_installed('disqus'):
        args.update({
            'comments_widget': comments.get_widget(driver_name='disqus')
        })

    return tpl.render('content/{}'.format(e.model), args)


def content_page_view(args: dict, inp: dict) -> str:
    """Single Page view.
    """
    return content_article_view(args, inp)


def _get_sidebar(exclude_ids: list) -> list:
    """Get sidebar content.
    """
    r = {
        'popular': _get_articles(exclude_ids, 3, sort_field='views_count', days=30),
        'latest': _get_articles(exclude_ids, 3, days=30),
        'tag_cloud': content.widget.TagCloud(
            uid='sidebar-tag-cloud',
            title=lang.t('tags_cloud'),
            css='block',
            term_css='hvr-sweep-to-right',
        ),
    }

    if plugman.is_installed('content_digest'):
        from plugins import content_digest
        r['content_digest_subscribe'] = content_digest.widget.Subscribe()

    return r


def _get_articles(exclude_ids: list, count: int = 6, section: content.model.Section = None,
                  sort_field: str = 'publish_time', days: int = None, starred: bool = False) -> list:
    """Get articles.
    """
    # Setup articles finder
    f = content.find('article').ninc('_id', exclude_ids).sort([(sort_field, odm.I_DESC)])

    # Filter by section
    if section:
        f.eq('section', section)

    # Filter by publish time
    if days:
        # Determine last published article date
        last_article = content.find('article').sort([('publish_time', odm.I_DESC)]).first()  # type: model.Article
        if last_article:
            f.gte('publish_time', last_article.publish_time - timedelta(days))
        else:
            f.gte('publish_time', datetime.now() - timedelta(days))

    # Filter by 'starred' flag
    if starred:
        f.eq('starred', True)

    r = []
    for article in f.get(count):
        # Show only articles which can be viewed by current user
        if article.check_permissions('view'):
            r.append(article)
        exclude_ids.append(article.id)

    return r
