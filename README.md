SSS Meetup 2016 website
=======================

This is the source code for the [SSS Meetup 2016 website](http://2016meet.sic.sssnet.tk),
but the code can be reused for organising other events in the future.
It has a landing page, a registration form and an alternate registration
form for newcomers. It also has a "Vote for the date" feature, described
below.

Voting for the date
===================
===================

In addition to the main registration form, this website also has an
additional view (not in the links but you can still see the code in
`app.py`) where people can vote for the most convenient dates. The idea
is that everybody votes for the all dates that are convenient for *them*,
and then a "best date" is chosen from the average of all the votes.

Setup
=====

To run the website, `cd` into the project directory and run

    pip install -r requirements.txt
    
to install the dependencies. Once dependencies are installed, you can
run the following command

    python app.py

to start up the development server.

License
=======
The source code for this website is licensed under the GPLv2 license; see
the LICENSE file for details. The website also uses other open-source
software libraries, which have their own individual licenses. Listed
below:

  * [bootstrap-datepicker](http://bootstrap-datepicker.readthedocs.io/)
    ([Apache License v2](https://github.com/eternicode/bootstrap-datepicker/blob/master/LICENSE))
    for the date voting
    for storing the registration and date vote info
  * [Skeleton](http://getskeleton.com) CSS framework
    ([MIT license](https://github.com/dhg/Skeleton/blob/master/LICENSE.md))
  * [FontAwesome](http://fontawesome.io)
    ([MIT license](http://fontawesome.io/license/)) for the fonts
  * [Stellar.js](http://markdalgleish.com/projects/stellar.js)
    ([MIT license](https://github.com/markdalgleish/stellar.js/blob/master/LICENSE-MIT))
    for the parallax scrolling animations

The website also makes use of [TinyDB](http://tinydb.readthedocs.org) and
the [Flask](http://flask.pocoo.org) framework.
    
