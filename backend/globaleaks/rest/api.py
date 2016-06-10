# -*- coding: UTF-8
#   API
#   ***
#
#   This file defines the URI mapping for the GlobaLeaks API and its factory
from cyclone import web

from globaleaks import LANGUAGES_SUPPORTED_CODES
from globaleaks.rest import requests
from globaleaks.settings import GLSettings
from globaleaks.handlers import exception, \
                                admin, receiver, custodian, \
                                public, \
                                submission, \
                                rtip, wbtip, \
                                files, authentication, token, \
                                export, l10n, wizard, \
                                base, user, shorturl

from globaleaks.handlers.admin import node as admin_node
from globaleaks.handlers.admin import user as admin_user
from globaleaks.handlers.admin import receiver as admin_receiver
from globaleaks.handlers.admin import context as admin_context
from globaleaks.handlers.admin import questionnaire as admin_questionnaire
from globaleaks.handlers.admin import step as admin_step
from globaleaks.handlers.admin import field as admin_field
from globaleaks.handlers.admin import l10n as admin_l10n
from globaleaks.handlers.admin import staticfiles as admin_staticfiles
from globaleaks.handlers.admin import overview as admin_overview
from globaleaks.handlers.admin import shorturl as admin_shorturl
from globaleaks.handlers.admin import statistics as admin_statistics
from globaleaks.handlers.admin import notification as admin_notification

from globaleaks.utils.utility import randbits

uuid_regexp      = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'

spec = [
    (r'/exception', exception.ExceptionHandler),

    ## Some Useful Redirects ##
    (r'/login', base.BaseRedirectHandler, {'url': '/#/login'}),
    (r'/admin', base.BaseRedirectHandler, {'url': '/#/admin'}),
    (r'/custodian', base.BaseRedirectHandler, {'url': '/#/custodian'}),


    ## Authentication Handlers ##
    (r'/authentication', authentication.AuthenticationHandler),
    (r'/receiptauth', authentication.ReceiptAuthHandler),

    ## Public API ##
    (r'/public', public.PublicResource),

    # Fake file hosting the Ahmia.fi descriptor
    (r'/description.json', public.AhmiaDescriptionHandler),

    # User Preferences Handler
    (r'/preferences', user.UserInstance),

    ## Token Handlers ##
    (r'/token', token.TokenCreate),
    (r'/token/' + requests.token_regexp, token.TokenInstance),

    # Shorturl Handler
    (requests.shorturl_regexp, shorturl.ShortUrlInstance),

    ## Submission Handlers ##
    (r'/submission/' + requests.token_regexp, submission.SubmissionInstance),
    (r'/submission/' + requests.token_regexp + r'/file', files.FileInstance),

    ## Receiver Tip Handlers ##
    (r'/rtip/' + uuid_regexp, rtip.RTipInstance),
    (r'/rtip/' + uuid_regexp + r'/comments', rtip.RTipCommentCollection),
    (r'/rtip/' + uuid_regexp + r'/messages', rtip.ReceiverMsgCollection),
    (r'/rtip/' + uuid_regexp + r'/identityaccessrequests', rtip.IdentityAccessRequestsCollection),
    (r'/rtip/' + uuid_regexp + r'/receivers', rtip.RTipReceiversCollection),
    (r'/rtip/' + uuid_regexp + r'/download/' + uuid_regexp, files.Download),
    (r'/rtip/' + uuid_regexp + r'/export', export.ExportHandler),

    ## Whistleblower Tip Handlers
    (r'/wbtip', wbtip.WBTipInstance),
    (r'/wbtip/comments', wbtip.WBTipCommentCollection),
    (r'/wbtip/receivers', wbtip.WBTipReceiversCollection),
    (r'/wbtip/upload', files.FileAdd),
    (r'/wbtip/messages/' + uuid_regexp, wbtip.WBTipMessageCollection),
    (r'/wbtip/' + uuid_regexp + r'/provideidentityinformation', wbtip.WBTipIdentityHandler),

    ## Receiver Handlers ##
    (r'/receiver/preferences', receiver.ReceiverInstance),
    (r'/receiver/tips', receiver.TipsCollection),
    (r'/rtip/operations', receiver.TipsOperations),

    (r'/custodian/identityaccessrequests', custodian.IdentityAccessRequestsCollection),
    (r'/custodian/identityaccessrequest/' + uuid_regexp, custodian.IdentityAccessRequestInstance),

    ## Admin Handlers ##
    (r'/admin/node', admin_node.NodeInstance),
    (r'/admin/node/logo', admin_staticfiles.NodeLogoInstance),
    (r'/admin/node/css', admin_staticfiles.NodeCSSInstance),
    (r'/admin/users', admin_user.UsersCollection),
    (r'/admin/users/' + uuid_regexp, admin_user.UserInstance),
    (r'/admin/users/' + uuid_regexp  + r'/img', admin_staticfiles.UserImgInstance),
    (r'/admin/contexts', admin_context.ContextsCollection),
    (r'/admin/contexts/' + uuid_regexp, admin_context.ContextInstance),
    (r'/admin/contexts/' + uuid_regexp  + r'/img', admin_staticfiles.ContextImgInstance),
    (r'/admin/questionnaires', admin_questionnaire.QuestionnairesCollection),
    (r'/admin/questionnaires/' + uuid_regexp, admin_questionnaire.QuestionnaireInstance),
    (r'/admin/receivers', admin_receiver.ReceiversCollection),
    (r'/admin/receivers/' + uuid_regexp, admin_receiver.ReceiverInstance),
    (r'/admin/notification', admin_notification.NotificationInstance),
    (r'/admin/notification/mail', admin_notification.EmailNotifInstance),
    (r'/admin/fields', admin_field.FieldCollection),
    (r'/admin/fields/' + uuid_regexp, admin_field.FieldInstance),
    (r'/admin/steps', admin_step.StepCollection),
    (r'/admin/steps/' + uuid_regexp, admin_step.StepInstance),
    (r'/admin/fieldtemplates', admin_field.FieldTemplatesCollection),
    (r'/admin/fieldtemplates/' + uuid_regexp, admin_field.FieldTemplateInstance),
    (r'/admin/shorturls', admin_shorturl.ShortURLCollection),
    (r'/admin/shorturls/' + uuid_regexp, admin_shorturl.ShortURLInstance),
    (r'/admin/stats/(\d+)', admin_statistics.StatsCollection),
    (r'/admin/activities/(summary|details)', admin_statistics.RecentEventsCollection),
    (r'/admin/anomalies', admin_statistics.AnomalyCollection),
    (r'/admin/staticfiles', admin_staticfiles.StaticFileList),
    (r'/admin/l10n/(' + '|'.join(LANGUAGES_SUPPORTED_CODES) + ')', admin_l10n.AdminL10NHandler),
    (r'/admin/staticfiles/([a-zA-Z0-9_\-\/\.]*)', admin_staticfiles.StaticFileInstance),
    (r'/admin/overview/tips', admin_overview.Tips),
    (r'/admin/overview/users', admin_overview.Users),
    (r'/admin/overview/files', admin_overview.Files),
    (r'/wizard', wizard.Wizard),

    ## Special Files Handlers##
    (r'/(favicon.ico)', base.BaseStaticFileHandler),
    (r'/robots.txt', public.RobotstxtHandler),
    (r'/s/(.*)', base.BaseStaticFileHandler),
    (r'/static/(.*)', base.BaseStaticFileHandler), # still here for backward compatibility
    (r'/l10n/(' + '|'.join(LANGUAGES_SUPPORTED_CODES) + ')', l10n.L10NHandler),

    (r'/x/timingstats', base.TimingStatsHandler),

    ## This Handler should remain the last one as it works like a last resort catch 'em all
    (r'/([a-zA-Z0-9_\-\/\.]*)', base.BaseStaticFileHandler, {'path': GLSettings.client_path})
]


class Application(web.Application):
    """
    This class simply overrides the web.Application.__class_ in order to
    allow to allow adding a prefix to the API urls.
    """
    def __call__(self, request):
        prefix = GLSettings.api_prefix
        if prefix != '' and request.path.startswith(prefix):
            request.path = request.path[len(prefix):]

        return web.Application.__call__(self, request)


def get_api_factory():
    settings = dict(cookie_secret=randbits(128),
                    debug=GLSettings.log_requests_responses,
                    gzip=True)

    GLAPIFactory = Application(spec, **settings)
    GLAPIFactory.protocol = base.GLHTTPConnection

    return GLAPIFactory
