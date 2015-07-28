# Executioner
A cross-language automation tool for running models.  **This project is currently in the planning stages.  Collaborators are welcome.**

**Objective:**

Many scientific and engineering fields often involve running models (e.g., a simulation engine), changing model inputs, and parsing model outputs.  Additionally, these model runs are often driven by other analytical tools. such as optimization, exploratory analysis, sensitivity analysis, etc.  Executioner aims to be an open source tool for connecting analytical tools to models and automating many repetitive tasks.

**Goals:**

1. Implementations in multiple programming languages (initially targeting Python, Java, and R)
2. Support simple templates with keyword substitutions
3. Provide a scripting language for more advanced automation
4. Enable parallel / batch processing

## Example API

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

    

## Scripting Language

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
