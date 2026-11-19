# Architecture

The engine separates scheduling from animation state and widget rendering. A scheduler per Tk interpreter drives active callbacks using `after`; animations calculate normalized progress from monotonic elapsed time and hand eased values to an update function. `Animator` and `tkanimator.animations` bind those values to supported widget operations. `Sequence`, `Parallel`, and `Timeline` compose animations without threads.

An animation state is `idle`, `running`, `paused`, `completed`, or `cancelled`. A completed or cancelled handle may be restarted with `restart()`. Cancellation removes its scheduler callback; the scheduler cancels its Tk timer when no callbacks remain. A destroyed widget raises `TclError`, which removes that callback safely.
