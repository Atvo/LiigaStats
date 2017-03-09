from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^moderate', hello.views.moderate),
    url(r'^shots', hello.views.shots_page),
    url(r'^update_filters', hello.views.update_filters),
    url(r'^update_table', hello.views.update_table),
    url(r'^add_match', hello.views.add_match),
    url(r'^add_all_matches_from_season', hello.views.add_all_matches_from_season),
    url(r'^init_work$', hello.views.init_work),
    url(r'^poll_state$', hello.views.poll_state, name="poll_state")
    #url(r'^admin/', include(admin.site.urls)),

)
