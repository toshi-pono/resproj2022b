clean:
	rm output/*

.PHONY: ats
ats:
	python simulate.py --node-type ats > output/ats.log

.PHONY: drift
drift:
	python simulate.py --node-type drift > output/drift.log

.PHONY: times
times:
	python simulate.py --node-type times > output/times.log

.PHONY: all
all: ats drift times
