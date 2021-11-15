# Scheduling you event(s)

[Framadate](https://framadate.org/) is a handy FOSS-alternative to doodle.

There is an instance hosted by the [Deutsches Forschungsnetz](https://www.dfn.de/dienstleistungen/dfnterminplaner/), addressing primarily German academia.

There is another one with a particular focus on privacy, offered by [Digitalcourage](https://nuudel.digitalcourage.de/).

The poll to 'Schedule an event' is immediately useful if you want to decide on one and just one date.

It's a bit trickier, if you want to organise a series of events and allocate the participants in accordance with their preferences.

If had this problem and tried to come up with a pragmatic solution.

# framadater.py

The script works with the [dfnterminplaner](https://www.dfn.de/dienstleistungen/dfnterminplaner/), but is probably easily adaptable to any other frama instance (just change the `service_url`).

* Just change the `poll_id` variable in the script and run the code `python3.9 framadater.py` or
* Run the code and copy the Poll ID into the Terminal.


The output is a list of names with the assigned date on the right.

# Limitations

I couldn't find (or think of) any alogrithm to accomplish the task, so I went for the brute force approach.

I calculate the variance for every possible combination.

The number of combinations is insanely high and it would literally take ages to finish.

However, by sorting the input (people with least 'yes' and least voted dates first) however, I could arrive at a reasonably homogeneous distribution
in reasonably litte time.

The solution is far from perfect, but it does its job.