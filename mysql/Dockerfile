FROM mysql:8.0

ENV MYSQL_DATABASE=django_db
ENV MYSQL_USER=django_user
ENV MYSQL_PASSWORD=secret
ENV MYSQL_ROOT_PASSWORD=secret

VOLUME /var/lib/mysql

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD mysqladmin ping --silent || exit 1