# IEWS(Immediate Earthquake Warning System)

## Introduction
System uses realtime earthquake data from IRIS. Still under active development.
The system is aimed to quickly analyze earthquake waveform and provide reliable earthquake warning.

## Usage
1. run pyslink2mseed_SLA.py to collect realtime waveform data from CI_SLA station.
2. run mseedAnalysis.py to plot waveform from last 10 minutes.


Note: The system cannot provide accurate magnitude analysis and warning at this stage

## Plan
The system will first focus on LA, US. Welcome more people to contribute to this repo.

## Credit
Part of the code is from @iannesbitt: https://github.com/iannesbitt/pyslink2mseed

## Resources
1. seedlink -> https://ds.iris.edu/ds/nodes/dmc/services/seedlink/
2. seismic stations search -> http://www.iris.washington.edu/gmap/#network=_REALTIME&planet=earth
