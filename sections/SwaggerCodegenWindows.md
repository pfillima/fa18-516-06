## Setting up Swagger Codegen on Windows 10 :smiley:

### Prerequisites

1. Windows 10 Operating System
2. Windows PowerShell
3. Java SE Development Kit 10

### Implementation

The following are steps to use Swagger-Codegen on a Windows 10 system.

1. Open Windows PowerShell

2. From the home directory, create a directory named *cloudmesh*, and change directories into it.

``` bash

> mkdir cloudmesh
> cd cloudmesh

```

3. Create a yaml file. For example the sample cpu.yaml file from 8.11.1.

4. From the directory cloudmesh, create a subdirectory named *swagger* and change directories into it.

``` bash

> mkdir swagger
> cd swagger

```

5. Download swagger-codegen-cli-2.3.1.jar using the following command in the /swagger directory

``` bash

> wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar

```

6. Finally, with a yaml file in /cloudmesh and swagger-codegen-cli-2.3.1.jar in the /cloudmesh/swagger directory, run the following command to generate the swagger-codegen output using python flask.

``` bash

> java -jar swagger-codegen-cli.jar generate -i ../cpu.yaml -l python-flask -o ../swagger_example/server/cpu/flaskConnection -D supportPython2=true

```

Now we see that within the /cloudmesh directory we have a *swagger_example* directory with subdirectories containing the codegen output.





