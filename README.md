# Executioner
A cross-language automation tool for running models.  **This project is currently in the planning stages.  Collaborators are welcome.**

**Objective:**

Many scientific and engineering fields often involve running computer models with varying model inputs.  The model inputs are often driven by analytical tools, such as optimization algorithms, exploratory modeling, sensitivity and factor analysis, etc.  Executioner aims to be an open source tool for automating the task of setting up a model's inputs, invokving the model, and processing the model outputs.

**Goals:**

1. Support simple templates with keyword substitutions
2. Provide a clean, programmatic way to define tasks
3. (Optional) Provide a scripting language for defining tasks
4. Enable parallel / batch processing across multiple cores or computers
5. Implementations in multiple programming languages (initially targeting Python, Java, and R)

## Examples:

Perform sensitivity analysis on a model using SALib.  This demonstrates sending inputs to and receiving outputs from an external process using standard I/O.

    from executioner import Executioner, ResultList
    from executioner.salib import *
    from SALib.sample import saltelli
    from SALib.analyze import sobol

    problem = {
        'num_vars': 11,
        'names': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11'], 
        'bounds': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], 
                   [0, 1], [0, 1], [0, 1]]
    }
    
    with Executioner() as executioner:
        executioner.onStart(Execute("python dtlz2.py"))
        executioner.add(WriteInput("${x1} ${x2} ${x3} ${x4} ${x5} ${x6} ${x7} ${x8} ${x9} ${x10} ${x11}\n"))
        executioner.add(ParseLine(type=float, name=["y1", "y2"]))
        executioner.onComplete(WriteInput("\n")) # send empty line to terminate process

        samples = saltelli.sample(problem, 1000, calc_second_order=True)
        Y = executioner.evaluateBatch(SALibSamples(problem, samples))
        sobol.analyze(problem, Y.to_nparray("y1"), print_to_console=True)

Executioner operates using tasks.  It defines many built-in tasks, or custom tasks can be developed by extending the Task class.  When constructing a job, tasks are partitioned into three types:

1. Startup tasks with `onStart`.  These are executed once when Executioner starts.
2. Per-evaluation tasks with `add`.  These tasks are executed once for every input being evaluated.
3. Completion or shutdown tasks with `onComplete`.  These are executed once when Executioner is closed.

