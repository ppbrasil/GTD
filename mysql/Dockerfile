FROM mysql:8.0

VOLUME /var/lib/mysql

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD mysqladmin ping --silent || exit 1