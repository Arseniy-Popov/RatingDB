#### About

* API for a database of titles characterised by categories and genres, users with roles and permissions, reviews on and ratings of titles, and comments on reviews. Documented at [redoc](http://api.ratingdb.arseniypopov.com/docs/redoc.html) / [swagger](http://api.ratingdb.arseniypopov.com/docs/swagger.html).
* provides the following entities: Title (Star Wars IV, etc.), Genre (sci-fi, etc), Category (movie, etc.), User (plain, admin, or moderator), Review ("my review: good stuff", score: 10/10, etc.), and Comment ("that's a good review").

#### Built with

- Built with `Python`, `Django REST Framework`, and `PostgreSQL`; tested with `pytest`.
- Deployed to [api.ratingdb.arseniypopov.com](http://api.ratingdb.arseniypopov.com/) with `AWS EC2`, `gunicorn`, and `nginx`; containerized with `Docker` and `docker-compose`.

#### Key parts
- [ratings/views.py](ratings/views.py)
- [ratings/models.py](ratings/models.py)
- [ratings/permissions.py](ratings/permissions.py)
- [ratings/roles.py](ratings/roles.py)