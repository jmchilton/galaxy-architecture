# Galaxy Production Deployment

> 📊 [View as training slides](../../../outputs/training-slides/generated/architecture-production/slides.html)

## Learning Questions
- How is Galaxy deployed in production?
- What is the difference between development and production setups?
- How does usegalaxy.org work?

## Learning Objectives
- Understand production deployment architecture
- Learn about PostgreSQL, nginx, and uWSGI
- Understand multi-process and multi-host setups
- Learn about usegalaxy.org infrastructure

## Production Galaxy - usegalaxy.org



#### Default

SQLite

Paste#http

Single process

Single host

Local jobs

---

#### Production

PostgreSQL

uWSGI / nginx

Multiple processes

Multiple hosts

Jobs across many clusters

[https://usegalaxy.org/production](https://usegalaxy.org/production)

## PostgreSQL

- Database server can scale way beyond default sqlite
- Supports concurrent connections from multiple Galaxy processes
- Better performance for production workloads
- [https://www.postgresql.org/](https://www.postgresql.org/)
- Configuration: `github.com/galaxyproject/usegalaxy-playbook` → `roles/galaxyprojectdotorg.postgresql`

## nginx (or Apache)

- Optimized servers for serving static content
- Reverse proxy to Galaxy application servers
- Load balancing across multiple Galaxy processes
- [https://www.nginx.com/resources/wiki/](https://www.nginx.com/resources/wiki/)
- Configuration: `github.com/galaxyproject/usegalaxy-playbook` → `templates/nginx/usegalaxy.j2`

## uWSGI

- Production-grade WSGI server
- Handles multiple Galaxy worker processes
- Better performance than development server
- Integrates well with nginx
- [https://uwsgi-docs.readthedocs.io/](https://uwsgi-docs.readthedocs.io/)

## Multi-processes

Threads in Python are limited by the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock).

Running multiple processes of Galaxy and separate processes for web handling
and job processing works around this.

This used to be an important detail - but uWSGI makes things a lot easier.

## Cluster Support

![Cluster Support](../_images/cluster_support.svg)

Galaxy can submit jobs to various cluster managers (Slurm, PBS, SGE, etc.)

## usegalaxy.org Web Architecture

![usegalaxy.org web servers](../_images/usegalaxy_webservers.svg)

## Complete usegalaxy.org Infrastructure

![usegalaxy.org servers](../_images/usegalaxyorg.svg)

Multiple web servers, job handlers, and compute clusters working together

## Key Production Considerations

- **Database**: Use PostgreSQL for production
- **Web Server**: Use nginx or Apache as reverse proxy
- **Application Server**: Use uWSGI or gunicorn
- **Processes**: Run multiple Galaxy processes
- **Job Handling**: Separate job handlers from web workers
- **Storage**: Use scalable object storage solutions
- **Monitoring**: Implement logging and monitoring
- **Backups**: Regular database and file backups

## Production Deployment Resources

- **Admin Training**: [https://training.galaxyproject.org/topics/admin/](https://training.galaxyproject.org/topics/admin/)
- **Galaxy Admin Docs**: [https://docs.galaxyproject.org/en/master/admin/](https://docs.galaxyproject.org/en/master/admin/)
- **Ansible Playbooks**: [https://github.com/galaxyproject/usegalaxy-playbook](https://github.com/galaxyproject/usegalaxy-playbook)
- **Community Support**: [https://help.galaxyproject.org/](https://help.galaxyproject.org/)

## Key Takeaways
- Production uses PostgreSQL instead of SQLite
- nginx/Apache serve static content, uWSGI runs Galaxy
- Multiple processes and hosts for scalability
- usegalaxy.org runs across multiple servers and clusters
