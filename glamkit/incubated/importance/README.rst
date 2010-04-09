==========
IMPORTANCE
==========

Importance is a generic way to (potentially) decide the order of model instances of several different types, if there is no more intuitive way.

Importance is represented by a simple FloatField called ``importance``. This app provides utilities 

Suggested importance rules
==========================

Importance has a logarithmic rank. The meanings of each rank depend on the information architecture for the site. For the NFSA site:

0.0 or less = not published (order could be used for prioritising edit lists, however)

0.0-1.0 = minor/archive content.

1.0-10.0 = published, unremarkable

10.0-100.0 = highlight in listings

100.0-1000.0 = feature in section landing page

1000.0 or greater = feature in homepage

etc.

Importance is a floating-point number, so it is usually possible to interpose an item between two others of differing importance.




Time-dependent importance
=========================

Consider a blog post. The importance of the post changes over time. The post is probably most important when it is first published, and tails off exponentially over time. We can define the rate of decay with a 'tenthlife', which is like halflife, only more intuitive to work with, given the importance rules above.

For example, a post in the 100-1000 range, with a tenthlife of 7 days, will fall into the 10-100 range after 7 days (ie it will drop by one rank every week, assuming the minimum rank is 0).

A blog post has maximum importance when it is first posted. The importance drops by 9/10ths towards the minimum with each *tenthlife* days since posting.

.. TODO: allow tenthlife to be overridden in each model instance. More important content should have a longer tenthlife.

Add it to a model like this:

::
@calculate_importance(spikes=("date_published",), tenthlife=7, max_importance=100, min_importance=1, importance_field="importance")
class Blog(models.Model):
    # Title, description, etc
    date_published = models.DateField(auto_now_add=True)
    importance = models.FloatField(editable=False, default=100)
::


Now, consider an event (or other item that is relevant to a period of time). The importance of an event changes over time. The event has 'spikes' of importance: when it is first announced, and when it is happening. The spike when it is first posted behaves the same way as that of a blog post. The spike when it is happening is more of a volcano shape, with importance increasing in the leadup to the event, and decreasing once the event has finished. At the moment, both spikes have the same tenthlife, and the overall importance is the maximum of the two measures.

A cron job updates importance measures every day (or other period of the user's choosing).
Setting up time-dependent importance

Add it to a model like this:

::
@calculate_importance(spikes=("date_published", ("start_date", "end_date") ), tenthlife=7, max_importance=1000, min_importance=1, importance_field="time_importance")
class Event(models.Model):
    # Title, description, etc
    date_published = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    time_importance = models.FloatField(editable=False, default=1000)
::

The reported importance *always* falls between the maximum and the minimum importance. If these are the same, then the importance is always the same.

Importance values are calculated for each ramp (in the ramp_up or ramp_down lists), with the same max/min importance and tenthlife for each. The maximum of these is the one that is used as the overall importance.