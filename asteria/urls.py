"""asteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from announcements.views import (
    AnnouncementListView
)
from django.conf.urls import (
    url,
    include,
)
from django.contrib import (
    admin
)

import challenges.views \
    as challenge_views
import teams.views \
    as team_views


urlpatterns = [
    url('', include('django.contrib.auth.urls')),

    url(r'^$', AnnouncementListView .as_view(), name='announcements'),

    url(r'^admin/', admin.site.urls),

    url(r'^categories/$'                , challenge_views.CategoryListView   .as_view(), name='categories' ),
    url(r'^category/(?P<slug>[-\w]+)/$' , challenge_views.CategoryDetailView .as_view(), name='category'   ),
    url(r'^challenge/(?P<slug>[-\w]+)/$', challenge_views.ChallengeDetailView.as_view(), name='challenge'  ),
    url(r'^challenges/$'                , challenge_views.ChallengeListView  .as_view(), name='challenges' ),
    url(r'^level/(?P<pk>\d{1,32})/$'    , challenge_views.LevelDetailView    .as_view(), name='level'      ),
    url(r'^levels/$'                    , challenge_views.LevelListView      .as_view(), name='levels'     ),
    url(r'^reveal_hint/$'               , challenge_views.reveal_hint                  , name='reveal_hint'),
    url(r'^submit_flag/$'               , challenge_views.submit_flag                  , name='submit_flag'),

    url(r'^appoint_captain/$'       , team_views.appoint_captain         , name='appoint_captain'     ),
    url(r'^change_team_name/$'      , team_views.change_team_name        , name='change_team_name'    ),
    url(r'^change_team_password/$'  , team_views.change_team_password    , name='change_team_password'),
    url(r'^join_team/$'             , team_views.join_team               , name='join_team'           ),
    url(r'^player/(?P<slug>[-\w]+)$', team_views.PlayerView    .as_view(), name='player'              ),
    url(r'^promote_demote/$'        , team_views.promote_demote          , name='promote_demote'      ),
    url(r'^register/$'              , team_views.register                , name='register'            ),
    url(r'^scoreboard/$'            , team_views.ScoreboardView.as_view(), name='scoreboard'          ),
    url(r'^team/(?P<slug>[-\w]+)$'  , team_views.TeamView      .as_view(), name='team'                ),
]

