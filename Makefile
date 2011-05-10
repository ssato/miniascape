REPO	= git@github.com:ssato/miniascape.git
BRANCH	= -b sid

WORKDIR	= ./m

makerpm	= cd $< && autoreconf -vfi && ./configure && make && make srpm && make rpm


all:


$(WORKDIR):
	git clone $(BRANCH) $(REPO) $(WORKDIR)

$(WORKDIR)/core: $(WORKDIR)

build: $(WORKDIR) build-core build-datasrc-dvd

build-core: $(WORKDIR)/core
	$(makerpm)

build-datasrc-dvd: $(WORKDIR)/datasrc/dvd
	$(makerpm)

gitclean: $(WORKDIR)
	cd $(WORKDIR) && git clean -f -d

.PHONY: build build-core build-datasrc-dvd gitclean
