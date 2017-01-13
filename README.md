# CAP-5771-Traffic-Prediction-National-Institute-of-Standards-and-Technology-Project

NIST IAD DSE Pilot Evaluation Plan
Version 1.6, Updated on July 1st, 2016

# Introduction

This document describes the plan for the National Institute of Standards and Technology (NIST) Information
Access Division (IAD) Data Science Evaluation (DSE) Series Pilot Evaluation to be held in
fall 2016. This pilot evaluation is a continuation and extension of the Data Science Pre-Pilot Evaluation
that was run in 2015, and precedes the first full evaluation of the DSE series. The primary goals
of the pilot are to:

a) further develop and exercise the evaluation process at NIST in the context of data science,
b) provide the opportunity to exercise in larger-scale evaluation,
c) serve as an archetype for the development of future evaluation tasks, datasets, and metrics,
d) establish baseline performance measurements,
e) bring to the fore new measurement methods and techniques that might be applied to a broad
range of use cases, regardless of data type and structure.

The pilot evaluation is set in the automotive traffic domain. This is because the domain is relevant to
a broad audience and because large amounts of data publicly available. However, it is expected that
many of the algorithms and techniques to be evaluated (as well as the evaluation approaches and
metrics themselves) will generalize to other domains.

The tasks in this evaluation are briefly enumerated below, with specific application to the traffic
domain as an example of each case.

1. Cleaning. Detecting and correcting errors, omissions, and inconsistencies in data or across
datasets, for example, detecting and correcting errors in traffic lane detector data flow values.

2. Alignment. Relating different representations of the same object, for example, matching traffic
events with traffic video segments containing those events.

3. Prediction. Making decisions about upcoming future values of a variable of interest, for example,
inferring the number and types of traffic incidents in an upcoming time interval based on
historical data.

4. Forecasting. Determining future (time-stamped) values of a variable within a given time interval,
e.g., determining traffic flow values for a set of lane detectors and their corresponding
timestamps.
