#### About

* API for a database of titles characterised by categories and genres, users with roles and permissions, reviews on and ratings of titles, and comments on reviews. Documented at [redoc](http://api.rating-db.arseniypopov.com/docs/redoc.html) / [swagger](http://api.rating-db.arseniypopov.com/docs/swagger.html).

#### Built with

- Built with `Python`, `Django REST Framework`, and `PostgreSQL`; tested with `pytest`.
- Deployed to [api.rating-db.arseniypopov.com](http://api.rating-db.arseniypopov.com/api/v1/) with `AWS EC2`, `gunicorn`, and `nginx`; containerized with `Docker` and `docker-compose`.

#### Key parts

- [ratings/views.py](ratings/views.py)
- [ratings/models.py](ratings/models.py)
- [ratings/serializers.py](ratings/serializers.py)
- [ratings/permissions.py](ratings/permissions.py)
- [ratings/roles.py](ratings/roles.py)
