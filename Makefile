REPO	= git@github.com:ssato/miniascape.git
BRANCH	= -b sid

WORKDIR	= ./m


all:


$(WORKDIR):
	git clone $(BRANCH) $(REPO) $(WORKDIR)

build: $(WORKDIR) build-core build-datasrc-dvd build-vmdata

build-core: $(WORKDIR)/core
	cd $(WORKDIR)/core && autoreconf -vfi && ./configure --enable-nginx && make && make rpm

build-datasrc-dvd: $(WORKDIR)/datasrc/dvd
	cd $(WORKDIR)/datasrc/dvd && autoreconf -vfi && ./configure && make && make rpm

build-vmdata:
	cd $(WORKDIR)/vmdata && autoreconf -vfi && ./configure && make && make rpm

gitclean: $(WORKDIR)
	cd $(WORKDIR) && git clean -f -d

.PHONY: build build-core build-datasrc-dvd build-vmdata gitclean
