# Simpy Review

1. Process Interaction

* wait for process

> env.timeout(3)

* interrupt

> env.process(car.run()).action.interrupt()

1. Shared Resources

* Basic Resource Usage


    The resource’s request() method generates an event that lets you wait until the resource becomes available again. If you are resumed, you “own” the resource until you release it.

    If you use the resource with the with statement as shown above, the resource is automatically being released. If you call request() without with, you are responsible to call release() once you are done using the resource.

> with bcs.request() as req:

1. how simpy works

    The environment stores these events in its event list and keeps track of the current simulation time.

    If a process function yields an event, SimPy adds the process to the event’s callbacks and suspends the process until the event is triggered and processed. When a process waiting for an event is resumed, it will also receive the event’s value.

1. events

    The value of a condition event is an ordered dictionary with an entry for every triggered event. In the case of AllOf,
    the size of that dictionary will always be the same as the length of the event list. The value dict of AnyOf will have at
    least one entry. In both cases, the event instances are used as keys and the event values will be the values.
    As a shorthand for AllOf and AnyOf, you can also use the logical operators & (and) and | (or):

1. Resources

    1. Resource

    1. PriorityResource, where queueing processes are sorted by priority

    1. PreemptiveResource, where processes additionally may preempt other processes with a lower priority
    
1.k

