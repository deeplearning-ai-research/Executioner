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
        executioner.tasks.add(CreateTempDir())
        executioner.tasks.add(Copy(from="~/model/"))
        executioner.tasks.add(Substitute(ignore="myModel"))
        executioner.tasks.add(Execute("./myModel -i inputs/config.xml"))
        executioner.tasks.add(ParseOutput("output.xml", outputParser))
        executioner.tasks.add(DeleteTempDir())

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

## Example Scripting Language

    Python Code:
        executioner = Executioner()
        executioner.loadScript("myScript.exs")
        executioner.evaluate({ "field1" = value1, "field2" = value2, ... })
        executioner.evaluateBatch([
            { "field1" = value11, "field2" = value12, ... },
            { "field1" = value21, "field2" = value22, ... },
            ...
        ])

    myScript.exs:
        temp = createTempDir()
        setWorkingDir(temp)
        
        copy(from="~/model/")
        substitute(ignore="myModel")
        execute("./myModel -i inputs/config.xml")
        output = parseXML("output.txt")
        
        delete(temp)
        return output.get("/root/model/output/value")

    

## Scripting Language Functions

`createTempDir()` - Create a new, empty temporary directory

`delete(...)` - Deletes a file or folder

`setWorkingDir(...)` - Sets the current working directory.  

`copy(from=..., to=...)` - Copies the file or directory to the working directory.

`substitute(file=..., ignore=...)` - Keyword substitution in the working directory.

`execute(...)` - Executes the given command within the working directory.

`parseCSV(...)` - Parses a CSV or other delimiter-separated file.  The returned object contains methods for accessing the entries in the CSV file.

`parseXML(...)` - Parses an XML file.  The returned object contains method for accessing the elements and attributes within the XML file, such as `parseXML("file.xml").get("/root/path/to/element")`.

`send(url=..., port=..., file=..., content=...)` - Transmits the raw contents of a file or string over sockets.

`receive(port=..., byline=...)` - Waits and reads from a socket.  If `byline` is true, then it reads only a single line from the socket.
