# Ecosystem

> 📊 [View as training slides](../../../outputs/training-slides/generated/architecture-ecosystem/slides.html)

## Learning Questions
- What projects make up the Galaxy ecosystem?
- How do different Galaxy projects interact?
- What tools are available for developers vs administrators?

## Learning Objectives
- Identify the major projects in the Galaxy ecosystem
- Understand the difference between user-facing and developer tools
- Learn about Galaxy communication channels

## Galaxy Ecosystem and Projects

*The architecture of the ecosystem.*

## Please Interrupt!

We're here to answer your questions about Galaxy architecture!

**Chat:** [galaxyproject Lobby](https://matrix.to/#/#galaxyproject_Lobby:gitter.im) (via Element)

**GitHub:** [github.com/galaxyproject ](https://github.com/galaxyproject)

**Twitter:** #usegalaxy, @galaxyproject

## The **/galaxyproject** projects

*The architecture of the ecosystem.*

## Matrix Community with Element

![galaxyproject Matrix Element community](../_images/element_galaxyproject.png)

Access via Element client or any Matrix client at [https://matrix.to/#/#galaxyproject_Lobby:gitter.im](https://matrix.to/#/#galaxyproject_Lobby:gitter.im)

More links we'll mention as we go through the slides:

- [https://matrix.to/#/#galaxyproject_Lobby:gitter.im](https://matrix.to/#/#galaxyproject_Lobby:gitter.im)
- [https://matrix.to/#/#galaxyproject_dev:gitter.im](https://matrix.to/#/#galaxyproject_dev:gitter.im)
- [https://matrix.to/#/#galaxyproject_admins:gitter.im](https://matrix.to/#/#galaxyproject_admins:gitter.im)
- [https://matrix.to/#/#galaxyproject_FederatedGalaxy:gitter.im](https://matrix.to/#/#galaxyproject_FederatedGalaxy:gitter.im)
- [https://matrix.to/#/#galaxyproject_bioblend:gitter.im](https://matrix.to/#/#galaxyproject_bioblend:gitter.im)
- [https://matrix.to/#/#galaxyproject_ephemeris:gitter.im](https://matrix.to/#/#galaxyproject_ephemeris:gitter.im)
- [https://matrix.to/#/#usegalaxy-eu_Lobby:gitter.im](https://matrix.to/#/#usegalaxy-eu_Lobby:gitter.im)
- [https://matrix.to/#/#galaxy-iuc_iuc:gitter.im](https://matrix.to/#/#galaxy-iuc_iuc:gitter.im)
- [https://matrix.to/#/#bgruening_docker-galaxy-stable:gitter.im](https://matrix.to/#/#bgruening_docker-galaxy-stable:gitter.im)
- [https://matrix.to/#/#Galaxy-Training-Network_Lobby:gitter.im](https://matrix.to/#/#Galaxy-Training-Network_Lobby:gitter.im)
- [https://matrix.to/#/#biocontainers_Lobby:gitter.im](https://matrix.to/#/#biocontainers_Lobby:gitter.im)
- [https://matrix.to/#/#bioconda_Lobby:gitter.im](https://matrix.to/#/#bioconda_Lobby:gitter.im)

Working group chats linked at [https://galaxyproject.org/community/wg/.](https://galaxyproject.org/community/wg/.)

**User-Facing Applications**

[galaxyproject/**galaxy** ](https://github.com/galaxyproject/galaxy)

The main Galaxy application.

Web interface, database model, job running, etc...

Also includes other web applications including the **ToolShed**.

[galaxyproject/**cloudlaunch** ](https://github.com/galaxyproject/cloudlaunch)

CloudLaunch web application to make it easy to launch images on a cloud, drives *[https://launch.usegalaxy.org*](https://launch.usegalaxy.org*)

[galaxyproject/**training-material** ](https://github.com/galaxyproject/training-material)

![logo](../_images/GTNLogo1000.png)

Galaxy training material for scientists, developers, and admins. Powers *[https://training.galaxyproject.org/*.](https://training.galaxyproject.org/*.)

[galaxyproject/**hub** ](https://github.com/galaxyproject/galaxy-hub)

The Galaxy Hub is the community and documentation hub for the Galaxy Project. It is maintained by the community through this GitHub repository. It is a static website built using the metalsmith static site generator.

Powers *[https://galaxyproject.org/*.](https://galaxyproject.org/*.)

[galaxyproject/**bioblend** ](https://github.com/galaxyproject/bioblend)

Official Python client for the Galaxy, ToolShed, and CloudMan APIs.

Best documented path to scripting the Galaxy API.

Galaxy API bindings for other languages, less actively maintained.

[galaxyproject/**cloudman**](https://github.com/galaxyproject/cloudman)

Galaxy CloudMan - a web application which manages a Galaxy Kubernetes cluster in
the cloud.

[**bgruening/docker-galaxy-stable** ](https://github.com/bgruening/docker-galaxy-stable)

High quality Docker containers for stable Galaxy environments.

Releases corresponding to each new version of Galaxy.

Many flavors available.

![Docker](../_images/docker-chart.png)

**For Plugin Developers**

[galaxyproject/**tools-iuc** ](https://github.com/galaxyproject/tools-iuc)

Galaxy tools maintained by the *IUC* ("Intergalactic Utilities Commission").

A variety of tools, generally of high quality including many of the core tools for Galaxy main.

Demonstrates *current tool development best practices* - development on
github and then deployed to test/main ToolSheds

[galaxyproject/**tools-devteam** ](https://github.com/galaxyproject/tools-devteam)

Many older tools appearing on usegalaxy.org.

## Tools Aside - More Repositories

Other repositories with high quality tools:

 * [Björn Grüning's repo](https://github.com/bgruening/galaxytools)
 * Peter Cock's repos:
   * [blast repo](https://github.com/peterjc/galaxy_blast)
   * [pico repo](https://github.com/peterjc/pico_galaxy)
   * [mira repo](https://github.com/peterjc/galaxy_mira)
 * [ENCODE tools](https://github.com/modENCODE-DCC/Galaxy)
 * [Biopython repo](https://github.com/biopython/galaxy_packages)
 * [Galaxy Proteomics repo](https://github.com/galaxyproteomics/tools-galaxyp)
 * [Greg von Kuster's repo](https://github.com/gregvonkuster/galaxy-csg)
 * [TGAC repo](https://github.com/TGAC/tgac-galaxytools)
 * [AAFC-MBB Canada repo](https://github.com/AAFC-MBB/Galaxy/tree/master/wrappers)
 * [Mark Einon's repo](https://gitlab.com/einonm/galaxy-tools)

[galaxyproject/**iwc** ](https://github.com/galaxyproject/iwc)

Intergalactic Workflow Commission. Hosting workflows and defining best practices for publishing workflows.

[https://matrix.to/#/#galaxyproject_iwc:gitter.im](https://matrix.to/#/#galaxyproject_iwc:gitter.im)

[galaxyproject/**planemo** ](https://github.com/galaxyproject/planemo)

Command-line utilities to assist in the development of Galaxy tools and workflows.
Linting, testing, deploying to ToolSheds...

*The best practice approach for Galaxy tool development!*

[galaxyproject/**planemo-machine** ](https://github.com/galaxyproject/planemo-machine)

Builds Galaxy environments for Galaxy tool development including Docker
container, virtual machines, Google compute images

[galaxyproject/**galaxy-language-server** ](https://github.com/galaxyproject/galaxy-language-server)

![Galaxy Language Server](https://github.com/galaxyproject/galaxy-language-server/raw/assets/snippets.gif)

Language server implementation for Galaxy tools. Visual Studio Code extension for tool development.

Test execution, code completion, best practices, documentation tooltips, etc..

[galaxyproject/**starforge** ](https://github.com/galaxyproject/starforge)

![StarForge logo](https://raw.githubusercontent.com/galaxyproject/starforge/master/docs/starforge_logo.png)

Build Galaxy framework dependencies as Python wheels when needed.

[galaxyproject/**cargo-port** ](https://github.com/galaxyproject/cargo-port)

![Cargo Port Logo](https://raw.githubusercontent.com/galaxyproject/cargo-port/master/media/cpc-plain-small.png)

Provides stable URLs and caching for application links, etc.. An important layer for reproducibility but largely transparent.

**For Deployers and Admins**

galaxyproject/**{ansible-\*, \*-playbook}**<br>
usegalaxy-eu/**{ansible-\*, \*-playbook}**

[Ansible](https://www.ansible.com/) components to automate almost every aspect of Galaxy installation and maintenance.

Ansible is an advanced configuration management system

These playbooks are used to maintain Galaxy main, cloud and Docker images, virtual machines, ...

[galaxyproject/**gravity** ](https://github.com/galaxyproject/gravity)

A process manager (supervisor) and management tools for Galaxy servers.

`galaxyctl` which is used to manage the starting, stopping, and logging of Galaxy's various processes.

`galaxy` which can be used to run a Galaxy server in the foreground.

[galaxyproject/**galaxy-helm** ](https://github.com/galaxyproject/galaxy-helm)

Kubernetes helm chart for deploying Galaxy. Leveraged by cloudlaunch and CloudMan but usable standalone.

[galaxyproject/**pulsar** ](https://github.com/galaxyproject/pulsar)

![Pulsar Logo](https://galaxyproject.org/images/galaxy-logos/pulsar_transparent.png)

Distributed job execution engine for Galaxy.

Stages data, scripts, configuration.

Can run jobs on Windows machines.

Can act as its own queuing system or access an existing cluster DRM.

[galaxyproject/**ephemeris** ](https://github.com/galaxyproject/ephemeris)

Library and CLI for managing Galaxy plugins - tools, index data, and workflows.

Layer on top of BioBlend building useful utilities for working with the Galaxy API from an administrator perspective.

[galaxyproject/**gxadmin** ](https://github.com/galaxyproject/gxadmin)

Handy command-line utility for Galaxy administrators.

## ephemeris vs gxadmin

Ephemeris generally talks to the Galaxy API and is a pure Python project, gxadmin talks directly to the Galaxy database and relevant files.

## Total Perspective Vortex

[galaxyproject/total-perspective-vortex **](https://github.com/galaxyproject/total-perspective-vortex)

![TPV Logo](https://raw.githubusercontent.com/galaxyproject/total-perspective-vortex/main/docs/images/tpv-logo-wide.png)

TotalPerspectiveVortex (TPV) provides an installable set of dynamic rules for the Galaxy application that can route entities (Tools, Users, Roles) to appropriate job destinations based on a configurable yaml file.

[**usegalaxy-eu/tiaas2 **](https://github.com/usegalaxy-eu/tiaas2)

![TIAAS Logo](https://raw.githubusercontent.com/usegalaxy-eu/tiaas2/master/images/tiaas-logo.png)

Django-based infrastructure for creating pools of users, etc.. for training events and connecting them to Galaxy.

## Some (out of many) friends of the project

![Bioconda](../_images/conda_logo.png)

![Biocontainers](../_images/biocontainers.png)

Check out dev training materials "Tool Dependencies and Conda" and "Tool Dependencies and Containers"
for more context.

## Putting it all together

![Large graphic showing different domains and where different portions of the Galaxy community can be found from Biology, Dev, Packaging, Deployment, Documentation, Training, and Support.](../_images/galaxy_main_scheme.png)

[galaxyproject/**galaxy** ](https://github.com/galaxyproject/galaxy)

The rest of the slides will focus on the core repository.

## Key Takeaways
- Multiple user-facing applications (Galaxy, CloudLaunch, Training Material)
- Developer libraries for plugin developers
- Admin tools for deployment
- Active community on Matrix (via Element client)
