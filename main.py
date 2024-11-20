"""
Introduction
to
ACT - R
The
following
notes
come
from two workshops

that
have
been
run
on
Python
ACT - R and cognitive
modelling in general: one
at
Ben - Gurion
University
of
the
Negev(March
2009) and one
at
the
University
of
Basel(August
2009).

I
am
interested in mechanistic
models
of
human
cognition
Strong
claim: the
steps
within
the
model
reflect
the
steps
within
actual
cognition
Why? Two
inter - related
reasons:
Needed
for predictions that cover a wide range of types of measurements (performance, reaction time, neural activity, effects of interventions, etc.)
Broad
ranges
of
predictions
seem
to
be
required if we
want
to
form
explanations
But
this
seems
like
it
would
open
up
so
many
more
possibilities
when
creating
a
model
Modelling
already
suffers
from having to

way
too
many
variables
Constraints
Have
performance, timing and neural
activity
predictions
all
come
from the same

variables( as much as possible)
Reaction
times
are
not just
another
output
of
the
model: Each
internal
step in the
model
must
take
a
certain
amount
of
time(although
steps
may
run in parallel).Reaction
time
predictions
must
be
based
on
combining
these
times.
Use
the
same
basic
components
for all models.
    The
    result is a
    cognitive
    architecture.
Ideally, once
we
have
a
solid
cognitive
architecture, we
can
make
a
model
for a new cognitive situation without first gathering any empirical data specifically about that situation.Our underlying theory of what the components are and how they are used constrains the creation of the model.
Another
way
to
look
at
this is that
the
cognitive
theory
acts
somewhat
like
a
Bayesian
prior.It
indicates
what
sort
of
models
are
likely
to
be
accurate.
We
can
use
empirical
evidence
about
this
specific
situation
to
help
further
specify
the
model.
This
evidence
will
be
more
important in areas
where
the
theory
does
not make
strong
claims
In
areas
where
the
cognitive
theory is well
established, we
might
trust
the
theory
even
more
than
our
empirical
observations(especially
with small sample sizes)
ACT - R
Long
term
project
to
develop
such
an
architecture
Used
for models of mathematical reasoning, serial recall, learning paired associates, human computer interaction, novice to expert transitions, semantic priming, n-back task, sleep deprivation, etc, etc
Initial
focus
on
behavioural and reaction
time
data, now
expanding
into
neural
predictions(BOLD, some
EEG)
The
most
widely
used and evaluated
cognitive
architecture
Basic
components: actr - modules.png
Production
system( if / then
rules) for executive control
    Separate
    modules
    running in parallel
    for everything else
A
set
of
equations
specifying
the
behaviour
of
these
components
Making
ACT - R
models
Many
researchers
just
make
models
by
writing
code
from scratch to

follow
the
equations
Since
there
are
a
common
set
of
components, libraries
exist
that
implement
these
Lisp
ACT - R is the
most
common;
directly
developed
by
core
ACT - R
researchers, integrates
a
lot
of
sensorimotor / HCI
theory as well(Fitts
' law, etc.)
Also
jACT - R and Python
ACT - R
We
'll be using Python ACT-R
Python
version
was
developed
to
expose
the
core
components
of
ACT - R, making
it
more
suitable
for connecting new components, integrating with other code
Lisp version seems to take new users most of a week to get into
Plus, I'm the primary author of the Python version
Everything in this session applies to all versions, except when
there
are
specific
code
examples.Python
ACT - R
uses
a
different
syntax, but is the
same
underlying
theory
Attachment
Size
actr - modules.png
37.84
KB
Representation in ACT - R
Chunks
One
chunk is a
set
of
slot - value
pairs
thing: cat
type: animal
size: small
skin: furry
tail: long
unofficial
limit
of
7 + -2
slots
per
chunk
Basis
of
representation
throughout
ACT - R
The
different
modules
use
chunks
to
pass
information
Buffers
A
small
number
of
data
stores, each
for a different purpose
Each
can
store
one
chunk
at
a
time
Each is a
physically
distinct
brain
location
Can
be
thought
of as "working memory"
Visual
Buffer
Symbolic
description
of
currently
visually
attended
object
shape: circle
color: red
size: large
"what"
pathway
Visual - Location
Buffer
Description
of
current
location
of
attention
"where"
pathway
Aural
Buffer
Manual
Buffer
Retrieval
Buffer
Currently
recalled
declarative
memory
chunk
name: Fluffy
animal: cat
owner: self
color: grey
Imaginal
Buffer
working
memory
scratchpad
Goal
Buffer
keeps
track
of
current
task
action: counting
current: three
goal: seven
Procedural
Memory in ACT - R
central
executive
control(serial
bottleneck
for cognition)
many
possible
actions
that
could
be
taken
now;
pick
one
selection
based
on
current
context(buffers) and a
set
of if -then
rules(productions)
actions
can
be
overt(press
a
button, more
gaze, turn
a
steering
wheel) or internal(recall
a
memory, change
information in working
memory, visualize
an
object)
Constraints:
The
"IF"
portion
specifies
a
pattern
that
must
be
present in the
buffers
The
"THEN"
portion
specifies
commands
to
send
to
modules and changes
to
chunks in buffers
50
msec
to
select and apply
a
production
If
multiple
productions
match, a
reinforcement
learning
system is used
to
select
one
action
A
utility is calculated
for each production, choose the one with the largest utility
no
strong
theory or evidence
for any particular RL system
original: U = PG - C
P = success / (success + failure)
C = time / (success + failure)
TD - learning
current: when
reward
R
occurs, all
recent
productions
get: U = U + a * (R - dt - U)
Examples
for Procedural Memory
    pm_1.py
The
simplest
possible
example
# initial code to set up Python ACT-R
import ccm
from ccm.lib.actr import *

log = ccm.log()


# define the model
class MyModel(ACTR):
    goal = Buffer()

    def greeting(goal='action:greet'):
        print
        "Hello"
        goal.clear()


# run the model        
model = MyModel()
ccm.log_everything(model)
model.goal.set('action:greet')
model.run()
One
single
production
called
greeting, which
fires if the
goal
chunk
has
a
slot
called
action
whose
value is greet
Clears
the
goal
afterward
so
that
the
same
production
doesn
't keep firing over and over
pm_2.py
Two
different
productions.One is selected
based
on
the
contents
of
the
goal
buffer.
# initial code to set up Python ACT-R
import ccm
from ccm.lib.actr import *

log = ccm.log()


# define the model
class MyModel(ACTR):
    goal = Buffer()

    def greeting1(goal='action:greet style:casual person:?name'):
        print
        "Hi", name
        goal.clear()

    def greeting2(goal='action:greet style:formal person:?name'):
        print
        "Greetings", name
        goal.clear()


# run the model        
model = MyModel()
ccm.log_everything(model)
model.goal.set('action:greet style:formal person:Terry')
model.run()
Syntax: ?x
indicates
that
the
value
may
be
used
by
the
THEN
portion
of
the
rule, but
can
match
anything
pm_3.py
Using
a
large
number
of
productions
sequentially.
# initial code to set up Python ACT-R
import ccm
from ccm.lib.actr import *

log = ccm.log(html=True)


# define the model
class ExpertCountingModel(ACTR):
    goal = Buffer()

    def countFromOne(goal='action:counting current:one target:!one'):
        goal.modify(current='two')

    def countFromTwo(goal='action:counting current:two target:!two'):
        goal.modify(current='three')

    def countFromThree(goal='action:counting current:three target:!three'):
        goal.modify(current='four')

    def countFromFour(goal='action:counting current:four target:!four'):
        goal.modify(current='five')

    def countFromFive(goal='action:counting current:five target:!five'):
        goal.modify(current='six')

    def countFromSix(goal='action:counting current:six target:!six'):
        goal.modify(current='seven')

    def countFromSeven(goal='action:counting current:seven target:!seven'):
        goal.modify(current='eight')

    def countFromEight(goal='action:counting current:eight target:!eight'):
        goal.modify(current='nine')

    def countFromNine(goal='action:counting current:nine target:!nine'):
        goal.modify(current='ten')

    def countFinished(goal='action:counting current:?x target:?x'):
        print
        'Finished counting to', x
        goal.clear()


# run the model        
model = ExpertCountingModel()
ccm.log_everything(model)
model.goal.set('action:counting current:one target:five')
model.run()
Examine
html
log
to
see
what is happening
Syntax: !x
says
to
not match if the
chunk
has
this
slot
value
Syntax: using ?x
twice
requires
the
same
value
for both slots
    Syntax: can
    also
    do !?x, requiring
    a
    different
    value
    for both slots
        pm_4.py
Using
multiple
buffers
# initial code to set up Python ACT-R
import ccm
from ccm.lib.actr import *

log = ccm.log(html=True)


# define the model
class ExpertCountingModel(ACTR):
    goal = Buffer()
    imaginal = Buffer()

    def countFromOne(goal='action:counting target:!one', imaginal='number:one'):
        imaginal.set('number:two')

    def countFromTwo(goal='action:counting target:!two', imaginal='number:two'):
        imaginal.set('number:three')

    def countFromThree(goal='action:counting target:!three', imaginal='number:three'):
        imaginal.set('number:four')

    def countFromFour(goal='action:counting target:!four', imaginal='number:four'):
        imaginal.set('number:five')

    def countFromFive(goal='action:counting target:!five', imaginal='number:five'):
        imaginal.set('number:six')

    def countFromSix(goal='action:counting target:!six', imaginal='number:six'):
        imaginal.set('number:seven')

    def countFromSeven(goal='action:counting target:!seven', imaginal='number:seven'):
        imaginal.set('number:eight')

    def countFromEight(goal='action:counting target:!eight', imaginal='number:eight'):
        imaginal.set('number:nine')

    def countFromNine(goal='action:counting target:!nine', imaginal='number:nine'):
        imaginal.set('number:ten')

    def countFinished(goal='action:counting target:?x', imaginal='number:?x'):
        print
        'Finished counting to', x
        goal.clear()


# run the model        
model = ExpertCountingModel()
ccm.log_everything(model)
model.goal.set('action:counting target:five')
model.imaginal.set('number:one')
model.run()
can
build
full
models
with just this
tends
to
be
for well - learned expert behaviours
pm_5.py
A
model
of
repeated
binary
choice
# initial code to set up Python ACT-R
import ccm
from ccm.lib.actr import *

log = ccm.log(html=True)


# define the model
class RepeatedBinaryChoiceModel(ACTR):
    goal = Buffer()

    pmnoise = PMNoise(noise=0.3)
    pm = PMNew(alpha=0.2)

    def pressA(goal='action:choose'):
        self.reward(0.3)

    def pressB(goal='action:choose'):
        self.reward(0.1)


# run the model        
model = RepeatedBinaryChoiceModel()
ccm.log_everything(model)
model.goal.set('action:choose')
model.run(limit=1.5)
might
be
a
model
of
an
extremely
well - practiced
participant, but
highly
unconstrained
since
it
's really just the RL system at play here
The
procedural
memory
system in ACT - R
acts
more as an
organizational
constraint
on
the
model
Attachment
Size
pm_1.py
356
bytes
pm_2.py
556
bytes
pm_3.py
1.49
KB
pm_4.py
1.63
KB
pm_5.py
533
bytes
Declarative
Memory in ACT - R
Fundamental
principle:
The
odds
of
a
memory
being
needed
decay as a
power
law
over
time
If
a
memory
occurs
more
than
once, these
odds
are
summed
over
all
occurrences
Reasonable
match
to
realistic
environments(Anderson & Schooler, 1991)
Implementation
A
memory
item is a
chunk
Each
chunk
has
an
activation
value
A: A = ln(sum(t ^ -d))
When
trying
to
recall
a
chunk, start
with a pattern constraints on the chunk, find all the chunks that match this pattern, recall the one with the highest activation.
Time
required
for recall: T = Fe ^ -A
Need
some
sort
of
randomness, so
add
noise
to
A.Traditionally, this
has
been
logistic
noise, but
could
also
be
normally
distributed.
Can
only
attempt
to
recall
one
chunk
at
a
time
If
A is too
low(below
threshold
T), then
recall
fails
Well - studied
chunks
end
up
with a fairly constant A value, plus effects of recent usage
Parameters
d = 0.5(consistent
across
all
ACT - R
models)
F = 0.05(indicates
50
msec
to
recall
a
chunk
with activation 0. Not particularly consistent across models)
s = 0.3(noise;
almost
always
between
0.2 - 0.5)
T = 0(recall
threshold;
usually - 3
to
0)
Declarative
Memory
Examples
dm_addition.py
Basic
example
of
adding
by
counting(5 + 2
by
doing
5, 6, 7)
import ccm
from ccm.lib.actr import *

log = ccm.log(html=True)


class Addition(ACTR):
    goal = Buffer()
    retrieve = Buffer()
    memory = Memory(retrieve, threshold=-3)
    DMNoise(memory, noise=0.3)

    def init():
        memory.add('count 0 1')
        memory.add('count 1 2')
        memory.add('count 2 3')
        memory.add('count 3 4')
        memory.add('count 4 5')
        memory.add('count 5 6')
        memory.add('count 6 7')
        memory.add('count 7 8')

    def initializeAddition(goal='add ?num1 ?num2 count:None?count sum:None?sum'):
        goal.modify(count=0, sum=num1)
        memory.request('count ?num1 ?next')

    def terminateAddition(goal='add ?num1 ?num2 count:?num2 sum:?sum'):
        goal.set('result ?sum')
        print
        sum

    def incrementSum(goal='add ?num1 ?num2 count:?count!?num2 sum:?sum',
                     retrieve='count ?sum ?next'):
        goal.modify(sum=next)
        memory.request('count ?count ?n2')

    def incrementCount(goal='add ?num1 ?num2 count:?count sum:?sum',
                       retrieve='count ?count ?next'):
        goal.modify(count=next)
        memory.request('count ?sum ?n2')


model = Addition()
ccm.log_everything(model)
model.goal.set('add 5 2 count:None sum:None')
model.run()
Over
time, doing
different
tasks, should
show
practice
effects(commonly
used
chunks
become
faster)
dm_rps.py
A
model
of
playing
rock
paper
scissors
Given
the
current
situation(the
last
two
moves
the
opponent
played), recall
a
past
experience
that
matches
this
pattern.
from ccm.lib.actr import *


class MemoryPlayer(ACTR):
    goal = Buffer()
    goal.set('play rps')

    imaginal = Buffer()
    imaginal.set('None None None')

    retrieval = Buffer()
    memory = Memory(retrieval)
    baselevel = DMBaseLevel(memory)
    noise = DMNoise(memory, 0.3)

    def start_recall(goal='play rps', choice='waiting:True', imaginal='?last ?last2'):
        goal.set('recall')
        memory.request('history ?last ?last2')

    def recall_fail_p(goal='recall', memory='error:True'):
        goal.set('choose paper')

    def recall_fail_r(goal='recall', memory='error:True'):
        goal.set('choose rock')

    def recall_fail_s(goal='recall', memory='error:True'):
        goal.set('choose scissors')

    def recall_success_r(goal='recall', retrieval='history ? ? rock'):
        goal.set('choose paper')

    def recall_success_p(goal='recall', retrieval='history ? ? paper'):
        goal.set('choose scissors')

    def recall_success_s(goal='recall', retrieval='history ? ? scissors'):
        goal.set('choose rock')

    def choose(goal='choose ?option'):
        choice.choose(option)
        goal.set('check response')

    def check_response(goal='check response', choice='opponent:?choice', imaginal='?last ?last2'):
        memory.add('history ?last ?last2 ?choice')
        retrieval.clear()
        imaginal.set('?last2 ?choice')
        goal.set('play rps')


Declarative
Memory
Variations
Spacing
Effect
d = ce ^ -A + a
More
accurate
match
to
memory
tasks
with lots of items
Individual
differences
captured
by
c and a
Used in commercial
memorization
tools
Partial
Matching
Sometimes
we
may
want
to
have
a
similarity
measure
between
slot
values
Attempting
to
recall
red
objects
may
lead
to
pink
objects
being
recalled
Modelled as an
activation
penalty
value
based
on
the
difference
between
the
target
slot
value and the
chunk
's slot value
-sum(P * M)
where
P is a
constant(possibly
different
per
slot) and M is a
programmer - specified
semantic
difference.
For
example,
if M(red,
     pink)=0.3 and P=1, then the chunk 'shape:circle color:pink' will have its activation reduced by 0.3 when attempting to recall chunks fitting the pattern 'color:red'
M = infinity
unless
otherwise
specified.
No
good
theoretical
guidelines
for setting this.Some people have used LSA, but no real consistent results.Pretty much just an ad-hoc method for getting semantic similarity into a model.
Spreading
Activation
Context
effect
on
memory: Thinking
about
a
topic
makes
facts
about
that
topic
easier
to
recall
The
chunks in working
memory
will
cause
related
chunks in declarative
memory
to
boost
their
activation
+sum(W * (S - ln(fan + 1)))
where
the
sum is over
the
values in a
buffer
chunk and fan is the
number
of
chunks in memory
that
contain
that
slot
value
dm_fan.py
import ccm
from ccm.lib.actr import *

log = ccm.log(html=True)


class FanModel(ACTR):
    goal = Buffer()
    retrieval = Buffer()
    memory = Memory(retrieval, latency=0.63)
    spread = DMSpreading(memory, goal)
    spread.strength = 1.6
    spread.weight[goal] = 0.5

    def init():
        memory.add('hippie in park')
        memory.add('hippie in church')
        memory.add('hippie in bank')
        memory.add('captain in park')
        memory.add('captain in cave')
        memory.add('debutante in bank')
        memory.add('fireman in park')
        memory.add('giant in beach')
        memory.add('giant in castle')
        memory.add('giant in dungeon')
        memory.add('earl in castle')
        memory.add('earl in forest')
        memory.add('lawyer in store')

    def start_person(goal='test ?person ?location'):
        memory.request('?person in ?')
        goal.set('recall ?person ?location')

    def start_location(goal='test ?person ?location'):
        memory.request('? in ?location')
        goal.set('recall ?person ?location')

    def respond_yes(goal='recall ?person ?location',
                    retrieval='?person in ?location'):
        print
        'yes'
        goal.clear()

    def respond_no_person(goal='recall ?person ?location',
                          retrieval='? in !?location'):
        print
        'no'
        goal.clear()

    def respond_no_location(goal='recall ?person ?location',
                            retrieval='!?person in ?'):
        print
        'no'
        goal.clear()


model = FanModel()
ccm.log_everything(model)
model.goal.set('test hippie park')
model.run()

Blending
False
memories: recalling
chunks
that
are not in memory
A
recalled
chunk
could
be
a
blending
of
the
chunks
that
could
be
recalled, weighted
by
activation
Not
clear
how
to
blend
symbolic
values
But
numerical
values
could
be
blended
Note: it is controversial
whether or not chunks
can
contain
numerical
values, and even if they
can
what
operations
should
be
supported
on
those
numerical
values
Could
be
simple
linear
weighted
averaging
This, plus
the
rock
paper
scissors
model
above, gave
the
model
that
won
the
Technion
Prediction
Tournament
dm_rbc.py


class SequentialModel(ACTR):
    goal = Buffer()
    goal.set('wait X')

    imaginal = Buffer()
    imaginal.set('A:None B:None')

    history = Buffer()
    history.set('None None')

    retrieval = Buffer()
    memory = BlendingMemory(retrieval, threshold=threshold)
    DMNoise(memory, noise=noise)
    DMBaseLevel(memory)

    if initialvalue is not None:
        for h in ['A A', 'A B', 'B A', 'B B']:
            memory.add('%s A %d' % (h, initialvalue))
            memory.add('%s B %d' % (h, initialvalue))

    def recallA(goal='wait X', top='waiting:True', imaginal='A:None', memory='busy:False error:False', history='?a ?b'):
        memory.request('?a ?b A ?')
        goal.set('wait A')

    def recallB(goal='wait X', top='waiting:True', imaginal='B:None', memory='busy:False error:False', history='?a ?b'):
        memory.request('?a ?b B ?')
        goal.set('wait B')

    def storeA(goal='wait A', top='waiting:True', imaginal='A:None B:?B', retrieval='? ? A ?reward'):
        # memory.add(retrieval)
        retrieval.clear()
        imaginal.set('A:?reward B:?B')
        goal.set('wait X')

    def storeB(goal='wait B', top='waiting:True', imaginal='B:None A:?A', retrieval='? ? B ?reward'):
        # memory.add(retrieval)
        retrieval.clear()
        imaginal.set('B:?reward A:?A')
        goal.set('wait X')

    def norecallA(goal='wait A', top='waiting:True', memory='error:True'):
        goal.set('choose A')

    def norecallB(goal='wait B', top='waiting:True', memory='error:True'):
        goal.set('choose B')

    def doEqualA(goal='wait', top='waiting:True', imaginal='A:?X!None B:?X'):
        goal.set('choose A')

    def doEqualB(goal='wait', top='waiting:True', imaginal='A:?X!None B:?X'):
        goal.set('choose B')

    def doUnEqual(goal='wait', top='waiting:True', imaginal='A:?A!None B:?B!None!?A'):
        if float(A) < float(B):
            goal.set('choose B')
        else:
            goal.set('choose A')

    def choose(goal='choose ?X', top='waiting:True'):
        top.choice(X)
        goal.set('reward ?X')

    def doReward(goal='reward ?X', top='reward:?reward!None', history='?a ?b'):
        memory.add('?a ?b ?X ?reward')
        goal.set('wait X')
        imaginal.set('A:None B:None')
        history.set('?b ?X')


Attachment
Size
dm_addition.py
1.2
KB
dm_rps.py
4.32
KB
dm_fan.py
1.54
KB
dm_rbc.py
5.78
KB
Sensory and Motor
Systems
inputs
from and outputs
to
the
world
lots
of
different
ones
driving
simulator
robot
control
typing and mouse
movement
visual
input
from computer screens

no
specific
theory
other
than
"use best available empirical data"
Motor
system
copied
from EPIC (Kieras & Meyer, 1996)
Fitts
' law for mouse and keyboard
motor
planning
time
separated
from action (so

actions
can
be
planned
but
not yet
initiated)
Visual
system
based
on
separating
"what" and "where"
pathways
vision_paired.py


class Paired(ACTR):
    goal = Buffer()
    retrieve = Buffer()
    memory = Memory(retrieve, threshold=-2, latency=0.35)
    DMBaseLevel(memory)
    DMNoise(memory, noise=0.5)

    visual = Buffer()
    location = Buffer()
    vision = Vision(visual, location)

    motor = Motor()

    def attendProbe(goal='state:start', vision='busy:False', location='?x ?y'):
        vision.examine('?x ?y')
        goal.modify(state='attendingProbe')
        location.clear()

    def detectStudyItem(goal='state:readStudyItem word:?w!None', vision='busy:False', location='?x ?y'):
        vision.examine('?x ?y')
        goal.modify(state='attendingTarget')
        location.clear()

    def associate(goal='state:attendingTarget word:?word!None num:?num', visual='type:Number text:?text'):
        memory.add('word:?word num:?text')
        visual.clear()
        goal.set('state:start word:None num:None')

    def readProbe(goal='state:attendingProbe word:None', visual='type:Text text:?word'):
        memory.request('word:?word')
        goal.modify(state='testing', word=word)
        visual.clear()

    def recall(goal='state:testing word:?word', retrieve='word:?word num:?num', motor='busy:False'):
        motor.press(num)
        goal.modify(state='readStudyItem')

    def cannotRecall(goal='state:testing word:?word', memory='error:True'):
        goal.modify(state='readStudyItem')


Programming
question
how
to
connect
the
model
up
to
a
simulation
of
the
environment?
Need
a
simulation
that
's equivalent to the one people used
Depends
a
lot
on
how
the
environment
was
developed
might
re - implement, might
directly
interface
Python
ACT - R
comes
with a simple system for making world objects and setting the properties that will appear in the visual buffer when that object is attended to
Simple
system
for defining motor actions, how long they take, and how they affect the environment
Attachment
Size
vision_paired.py
2.93
KB
"""
from python_actr import *


class TowersOfHanoi(ACTR):
    goal = Buffer()
    retrieve = Buffer()
    memory = Memory(retrieve, threshold=-2, latency=0.35)
    #DMBaseLevel(memory)
    #DMNoise(memory, noise=0.5)

    def start(goal='state:start'):
        # Initialize the board state
        goal.set('state:move n:3 from:source to:target using:auxiliary')

    def moveDisk(goal='state:move n:?n from:?from_ to:?to using:?using!None'):
        print(f"Move disk from {from_} to {to}")
        n = int(n)
        if n > 1:
            # Break move down into sub-moves
            # Move n-1 disks from 'from' to 'using' using 'to' as auxiliary
            memory.add(f'state:move n:{n - 1} from:{from_} to:{using} using:{to}')
            # Move the nth disk from 'from' to 'to'
            goal.set(f'state:moveDisk from:{from_} to:{to}')
        else:
            # Base case: move the single disk from 'from' to 'to'
            goal.set(f'state:moveDisk from:{from_} to:{to}')

    def moveDisk2(goal='state:moveDisk from:?from_ to:?to'):
        print(f"Move disk from {from_} to {to}")
        # Correcting the pattern to include named slots
        memory.request('state:move n:?n from:?from_ to:?to using:?using')
        goal.modify(state='moveNextDisk')

    def moveNextDisk(goal='state:moveNextDisk'):
        # Correcting the pattern to include named slots
        memory.request('state:move n:?n from:?from_ to:?to using:?using')
        goal.modify(state='move n:?n from:?from_ to:?to using:?using')

    def recallMove(goal='state:move n:?n from:?from_ to:?to using:?using'):
        goal.set(f'state:move n:{n} from:{from_} to:{to} using:{using}')


# To run the model
hanoi_model = TowersOfHanoi()
hanoi_model.goal.set('state:start')
hanoi_model.run()


# while hanoi_model.goal.state != 'done':
#    hanoi_model.cycle()
