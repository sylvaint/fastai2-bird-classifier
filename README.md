# fastai2 bird classifier

Bird classifier web app with the new fastai2 library.
Back end is my favorite web framework [Mojolicious](https://www.mojolicious.org/).
Front end is Vuejs.

## Deployed Application

You can find the deployed app [here](https://birds.smbtraining.com/bird_name)

## Deployment

The app was deployed on a CENTOS 7 server using Cloudflare as a DNS/Firewall and an Apache reverse proxy setup.
Instructions should be almost the same for any linux server or for MACOS.

### Prerequisites
* Conda with a python 3 installation
* fastai2 library
* startlette library
* uvicorn library
* ipykernel library
* aiohttp library
* Perl
* Mojolicous Web framework


```
$ pip install fastai2 uvicorn ipykernel aiohttp
$ conda install -c conda-forge starlette
$ curl -L http://install.perlbrew.pl | bash
$ perlbrew install-cpanm
$ perlbrew install perl-5.30.2
$ curl -L https://cpanmin.us | perl - -M https://cpan.metacpan.org -n Mojolicious
```

### Running

```
$ python birds.py serve >> ./log/birds.log
$ hypnotoad birds_mojo.pl
```
