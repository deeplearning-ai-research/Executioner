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

## Example APIs

    Python:
        from executioner import Executioner
        import xml.etree.ElementTree as ET

        def outputParser(file):
            tree = ET.parse(file)
            return float(tree.find("/root/results/value").text)

        executioner = Executioner()
        executioner.add(CreateTempDir())
        executioner.add(Copy(from="~/model/"))
        executioner.add(Substitute(ignore="myModel"))
        executioner.add(Execute("./myModel -i inputs/config.xml"))
        executioner.add(ParseOutput("output.xml", outputParser))
        executioner.add(DeleteTempDir())

        executioner.evaluateBatch([
            { "field1" = value11, "field2" = value12, ... },
            { "field1" = value21, "field2" = value22, ... },
        ])
        
    Java:
        Executioner executioner = new Executioner();
        executioner.add(new CreateTempDir());
        executioner.add(new Copy("~/model/"));
        executioner.add(new Substitute().ignore("myModel"));
        executioner.add(new Execute("./myModel -i inputs/config.xml"));
        executioner.add(new ParseOutput("output.xml", outputParser));
        executioner.add(new DeleteTempDir());

        executioner.withExecutorService(Executors.newFixedThreadPool(
            Runtime.getRuntime().availableProcessors()));

        executioner.evaluateBatch(...)
        
    R:
        executioner(
            tasks=list(
                CreateTempDir(),
                Copy(from="~/model/"),
                Substitute(ignore="myModel"),
                Execute("./myModel -i inputs/config.xml"),
                ParseOutput("output.xml", outputParser),
                DeleteTempDir()),
            evaluate=list(
                c(field1=value1, field2=value2)))
                
## Use Cases

### Passing Arguments on Command Line

    executioner = Executioner()
    executioner.add(Execute("./myModel -a ${field1} -b ${field2}"))

### Inputting to Standard Input / Reading from Standard Output

    executioner = Executioner()
    executioner.add(Execute("./myModel"))
    executioner.add(WriteInput("a: ${field1}\nb: ${field2}"))
    executioner.add(ParseOutput(outputParser)) # outputParser is a function reading from a stream
    
### Write Input File

    executioner = Executioner()
    executioner.add(WriteFile("input.json", "{ \"a\"=${field1}, \"b\"=${field2} }"))
    executioner.add(Execute("./myModel -i input.json"))
    
### Error Handling

    executioner = Executioner()
    executioner.add(Execute("./myModel"))
    executioner.add(CheckExitCode(ok=0)) # raises error if exit code != 0
    
### String Replacement

    executioner = Executioner()
    executioner.add(CreateTempDir())
    executioner.add(Copy(from="~/program/"))
    executioner.add(Substitute()) # scans all files in temp directory and replaces ${keywords}
    executioner.add(Execute("./myModel"))
    executioner.add(DeleteTempDir())
    
### Sockets

In this example, we start a long-running process that will process all inputs.  Each input is sent to the process on port 3088 and the output is received on one line.  The process ends when we send an empty input line.

    executioner = Executioner()
    executioner.onStart(Execute("./myModel -p 3088"))
    executioner.add(Send("${field1} ${field2}\n", server='localhost', port=3088))
    executioner.add(Receive(numlines=1))
    executioner.add(ParseOutput(outputParser))
    executioner.onComplete(Send("\n", port=3088))

### Parallelization

One option for parallelization is spawning a new model for each input:

    executioner = Executioner()
    executioner.distributeOnAllCores()
    executioner.add(Execute("./myModel -a ${field1} -b ${field2}"))
    
If the model implementation allows sending multiple inputs, such as over sockets or by standard input/output, Executioner will spawn one instance of the model for each core but distribute the model evaluations across all instances:

    executioner = Executioner()
    executioner.distributeOnAllCores()
    executioner.onStart(Execute("./myModel -p ${PORT}"))
    executioner.add(Send("${field1} ${field2}\n", server=${SERVER}, port=${PORT}))
    executioner.add(Receive(numlines=1))
    executioner.add(ParseOutput(outputParser))
    executioner.onComplete(Send("\n", port=${PORT}))
    
If sockets are used, Executioner will fill in the appropriate values for `${SERVER}` and `${PORT}` for each process.
    
Suppose we are running on 4 cores.  Executioner will spawn the program `myModel` 4 times, each with a different port.  Then, it invokes the `Send`, `Receive`, and `ParseOutput` for each model input.  The work will be evenly distributed across all 4 processes.  Finally, once all model inputs are evaluated, it sends the terminate signal (an empty line) to the 4 processes.
