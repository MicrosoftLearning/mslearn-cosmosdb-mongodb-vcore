## Data migration is a critical step in the process of moving from an existing MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account. While there are several ways to migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account, this lab focuses on using the MongoDB native tools to migrate the database. The MongoDB native tools are the most common way to migrate a MongoDB database to another. Most MongoDB administrators and developers are familiar with these tools.

# While this lab uses the MongoDB community edition, similar migration steps can be used for other MongoDB editions.

# Objectives

In this lab, you learn how to use the MongoDB native tools to migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account. You use the following tools:

* mongodump: This tool is used to dump the data from the local MongoDB server into a BSON (Binary JSON) file.
* mongorestore: This tool is used to restore the dumped data into the vCore-based Azure Cosmos DB for MongoDB server.

# Build your own lab environment

If you need to build your own lab environment, you need the following components and resource access.

* Visual Studio Code: Ensure Visual Studio Code is installed on your machine.
* Azure Subscription: Have access to an Azure Subscription for creating necessary resources.

# Clone the Repository

* Open Visual Studio Code.
* Press CTRL+SHIFT+P to open the command palette.
* Run Git: Clone and clone the repository https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git.
* Navigate to the cloned repository directory.
* Right-click on the 02-migrate folder and select Open in integrated Terminal.
# Create Azure Resources

You need access to the following Azure resources for this lab:
* vCore-based Azure Cosmos DB for MongoDB account

You can create these resources via the Azure portal or use the create-azure-resources.ps1 PowerShell script with the *.env file. Don't use existing production resources for this lab or any lab.

# Use the .env file

This file must either be populated manually, or by the create-azure-resources.ps1 script before you can run your application, since it contains the connection information to your Azure resources.

This file is both used to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs. It's the easiest way to prepopulate your resource information. The file is used to store the environment variables for your Azure Cosmos DB and Azure OpenAI account.

If you already have an existing Resource Group, a vCore-based Azure Cosmos DB for MongoDB account, an Azure Storage Account or an Azure Log Analytics workspace that you would like to use, just fill in those values in the .env file and set the skip create option for that resource to true. By default, the create-azure-resources.ps1 script uses this file to retrieve the necessary environment variables. Note that the create-azure-resources.ps1 script will populate the environment variables with default values if not specified in the .env file.

To learn more about the .env file and its parameters, review the .env file documentation.

# Use the create-azure-resources.ps1 script

"You don't need to run the create-azure-resources.ps1 script and can skip to the next section if you already have the necessary Azure resources created."

If you aren't using existing resources, or you aren't creating them through the Azure portal, this script creates the necessary Azure resources for this lab. It gives you the flexibility to create some or all of the resources required for this lab. You can either run the script as is or modify it to suit your needs. The resources created by the script include:

* Resource Group
* vCore-based Azure Cosmos DB for MongoDB account

The script has a rich set of parameters to help you customize the resources to be created. It also uses an .env file to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs.

" While these parameters can be passed directly to the script, we recommend you use the .env file to prepopulate your resource information instead of adding the parameters when executing the script. This will make it easier for you to manage your environment variables. "

To learn more about the PowerShell script and its parameters, review the create-azure-resources.ps1 documentation.

" Make sure the tenant, location and subscription you use allows for the creation of the necessary resources. Not all locations and subscriptions might allow or support the creation of all the required resources needed for this lab. If you encounter any issues, please reach out to your Azure Administrator. "

# Run the create-azure-resources.ps1 script to create the necessary Azure resources

To create the necessary Azure resources for this lab:

1. Run the following command in the integrated terminal.

powershell
az login
./create-azure-resources.ps1

2. Copy and save the environment variables returned by the script in case you need them later. You can verify the resources created in the Azure portal.

3. Make sure that the .env file is populated with the resource information.

" The vCore-based Azure Cosmos DB for MongoDB account will need a firewall rule to allow access from your current public IP address. If your Azure Cosmos DB account was generated by the create-azure-resources.ps1 script, it should have created the firewall rule for you. Check the existing firewall rules under the Networking Setting section of the Azure Cosmos DB Account. If you are not sure what your current public IP address is, you can use the following command to find out: "
powershell
Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get
Once the resources are created and your .env file is populated with the resource information, you can proceed to the next step.

# Install and load data into the MongoDB community edition on your local machine
Unless you have a nonproduction MongoDB server installed with access the internet, let's install the MongoDB community edition on your local machine. For more information on how to do this installation, review the instructions in the official MongoDB documentation.

# Install the MongoDB community edition
Let's install the MongoDB community edition on your local machine.

1. Open your browser and go to the MongoDB Community Server Download page from the official MongoDB website.

3. Select the Select package button and select the proper settings for your environment. For example, if you're using Windows, select the Windows x64 platform and the msi package.

| Version | 6.0.14 | | Platform | Your current OS/Platform | | Package | Your current install package type |

3. Select the Download button to download the installer.

4. Once the installer is downloaded, run the installer and follow the installation instructions for a Complete install.

* Choose all default options.
* Service name should be MongoDB.
* Select to Install MongoDB Compass.

This install should take a few minutes to complete.

5. Once the installation is complete, select the Finish button to close the installer if needed.

# Install the MongoDB Database Tools
We need a few tools to help us with the migration process. Let's install the MongoDB database tools on your local machine.

1. Open your browser and go to the MongoDB Command Line Database Tools Download page from the official MongoDB website.

2. Select the proper settings for your environment. For example, if you're using Windows, select the Windows x86_64 platform and the msi package.
| Version | 100.9.4 or the latest version | | Platform | Your current OS/Platform | | Package | Your current install package type |

3. Select the Download button to download the installer.

4. Once the installer is downloaded, run the installer and follow the installation instructions for a Complete install. Choose all default options.

5. Once the installation is complete, select the Finish button to close the installer if needed.

# Time to verify the installation.

1. Close Visual Studio Code and reopen it to ensure the environment variables are loaded.

2. Right-click on the 02-migrate folder and select Open in integrated Terminal.

3. In the terminal windows, run the following command to verify the installation:
If the server is up and running, it will reply every second or so, if it's down, it will eventually time out after around a minute.
If the server is down, follow the instructions in the official MongoDB documentation to start the server.

" While the installation of MongoDB and its tools should have updated your PATH environment variable, if the command is not found, specify the path when calling the mongostat command. For example, if you installed the tools in the default location in the Windows environment, you can run the following command to verify the installation (replace the path with the actual path where the tools were installed and use that path in the other MongoDB Tools commands in this lab): "
bash
& "C:\Program Files\MongoDB\Tools\100\bin\mongostat"
We should now have a running MongoDB server on your local machine. Let's load some data into it.

# Load data into the MongoDB community edition
1. Open a new terminal and navigate to the MongoDB Tools installation folder.

2. Run the following command to load the sample data into the MongoDB server:

" bash
& mongoimport --host localhost --port 27017 --db cosmicworks --collection customers --jsonArray --file ../data/cosmicworks/customers.json
& mongoimport --host localhost --port 27017 --db cosmicworks --collection products --jsonArray --file ../data/cosmicworks/products.json
& mongoimport --host localhost --port 27017 --db cosmicworks --collection salesOrders --jsonArray --file ../data/cosmicworks/salesOrders.json "

This command loads the sample data into the MongoDB server running on your local machine.

We should now have a running MongoDB server with some data into it, it's time to migrate it to vCore-based Azure Cosmos DB for MongoDB.

# Migrate to a vCore-based Azure Cosmos DB for MongoDB account using MongoDB native tools (offline)

To export the data from the local MongoDB server and import it into the vCore-based Azure Cosmos DB for MongoDB account, you use the MongoDB mongodump and mongorestore native tools. In a production environment, if your database is large, you might need to search for other ways to migrate the database like through Azure Data Migration Service.

1. Dump the data from your local MongoDB server into a BSON file. Run the following command in the terminal:

bash
& mongodump --host localhost --port 27017 --db cosmicworks --out ../data/cosmicworks
This command creates a BSON file in the ../data/cosmicworks folder. The mongodump command outputs the progress of the dump operation.

2. Restore the dumped data into your vCore-based Azure Cosmos DB for MongoDB server. Replace , , yourMongoDBClusterName, and yourDatabaseName with your actual username, password, Azure MongoDB cluster name, and database name:

bash
& mongorestore --uri "mongodb+srv://<user>:<password>@yourMongoDBClusterName.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000" --db cosmicworks1 ../data/cosmicworks/cosmicworks
This command restores the BSON file into your vCore-based Azure Cosmos DB for MongoDB server. The mongorestore command outputs the progress of the restore operation.

" Don't forget to make sure the firewall rules for your vCore-based Azure Cosmos DB for MongoDB account are set to allow access from your current public IP address. If your Azure Cosmos DB account was generated by the create-azure-resources.ps1 script, it should have created the firewall rule for you. Check the existing firewall rules under the Networking Setting section of the vCore-based Azure Cosmos DB for MongoDB account. If you are not sure what your current public IP address is, you can use the following command to find out: "
powershell
Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get

# Let's verify the migration completed successfully.

1. Open the MongoDB Compass application.
2. Connect to your vCore-based Azure Cosmos DB for MongoDB connection string.
3. Select Continue on the warning screen.
4. You should see your database, collections, and documents in the left-hand navigation pane.
5. Close the MongoDB Compass application.

" Note that while you used the mongodump and mongorestore tools to migrate the data from your local MongoDB server to the vCore-based Azure Cosmos DB for MongoDB account, we could have also use mongoexport and mongoimport tools to do the same. "

You should now have a running vCore-based Azure Cosmos DB for MongoDB server with the data from your local MongoDB server. You successfully migrated the data from your local MongoDB server to the vCore-based Azure Cosmos DB for MongoDB account using the MongoDB native tools.

# Clean Up
After completing the lab exercises, it's important to clean up any resources you created to avoid incurring unnecessary costs. Here's how:

1. Azure Portal: Sign in to the Azure portal.

2. Delete Resource Group: If you created a new resource group for this lab, navigate to Resource groups, find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DB instance and any Azure OpenAI resources.

3. Manually Delete Individual Resources: If you added resources to an existing group, you need to delete each resource individually. Navigate to each resource created for this lab (for example, Azure Cosmos DB for MongoDB, Azure OpenAI account) and delete them.

4. Verify Deletion: Confirm all resources you no longer need were successfully removed and are no longer listed in your Azure portal.

5. Review Billing: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources were successfully deleted.

This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.

# Conclusion

You successfully migrated a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account using the MongoDB native tools. There are several other ways to migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account, including using Azure Data Studio for offline migrations and Azure Databricks for online/offline migrations. The method you choose depends on your specific requirements and constraints.

---------------------------------------------------------------------------------------------------------

## ESPAÑOL

## La migración de datos es un paso crítico en el proceso de pasar de una base de datos MongoDB existente a una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual. Si bien hay varias formas de migrar una base de datos MongoDB a una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual, esta práctica de laboratorio se centra en el uso de las herramientas nativas de MongoDB para migrar la base de datos. Las herramientas nativas de MongoDB son la forma más común de migrar una base de datos MongoDB a otra. La mayoría de los administradores y desarrolladores de MongoDB están familiarizados con estas herramientas.

# Si bien esta práctica de laboratorio utiliza la edición comunitaria de MongoDB, se pueden utilizar pasos de migración similares para otras ediciones de MongoDB.

# Objetivos

En este laboratorio, aprenderá a usar las herramientas nativas de MongoDB para migrar una base de datos de MongoDB a una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual. Utiliza las siguientes herramientas:

* mongodump: esta herramienta se utiliza para volcar los datos del servidor MongoDB local en un archivo BSON (JSON binario).
* mongorestore: esta herramienta se utiliza para restaurar los datos volcados en el servidor Azure Cosmos DB para MongoDB basado en núcleo virtual.

# Construya su propio entorno de laboratorio

Si necesita crear su propio entorno de laboratorio, necesita los siguientes componentes y acceso a recursos.

* Visual Studio Code: asegúrese de que Visual Studio Code esté instalado en su máquina.
* Suscripción de Azure: tenga acceso a una suscripción de Azure para crear los recursos necesarios.

# Clonar el repositorio

* Abra el código de Visual Studio.
* Presione CTRL+MAYÚS+P para abrir la paleta de comandos.
* Ejecute Git: clonar y clonar el repositorio https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git.
* Navegue hasta el directorio del repositorio clonado.
* Haga clic derecho en la carpeta 02-migrate y seleccione Abrir en Terminal integrada.
# Crear recursos de Azure

Necesita acceso a los siguientes recursos de Azure para este laboratorio:
* Cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual

Puede crear estos recursos a través de Azure Portal o usar el script de PowerShell create-azure-resources.ps1 con el archivo *.env. No utilice recursos de producción existentes para este laboratorio ni para ningún laboratorio.

# Usa el archivo .env

Este archivo debe completarse manualmente o mediante el script create-azure-resources.ps1 antes de poder ejecutar su aplicación, ya que contiene la información de conexión a sus recursos de Azure.

Este archivo se utiliza para recuperar y almacenar las variables de entorno necesarias tanto para el script de PowerShell como para las API de la aplicación de búsqueda vectorial. Es la forma más sencilla de completar previamente la información de sus recursos. El archivo se usa para almacenar las variables de entorno de su cuenta de Azure Cosmos DB y Azure OpenAI.

Si ya tiene un grupo de recursos existente, una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual, una cuenta de Azure Storage o un área de trabajo de Azure Log Analytics que le gustaría usar, simplemente complete esos valores en el archivo .env y configure el omita la opción de creación para ese recurso en verdadero. De forma predeterminada, el script create-azure-resources.ps1 usa este archivo para recuperar las variables de entorno necesarias. Tenga en cuenta que el script create-azure-resources.ps1 completará las variables de entorno con valores predeterminados si no se especifican en el archivo .env.

Para obtener más información sobre el archivo .env y sus parámetros, revise la documentación del archivo .env.

# Utilice el script create-azure-resources.ps1

"No es necesario ejecutar el script create-azure-resources.ps1 y puede pasar a la siguiente sección si ya tiene creados los recursos de Azure necesarios".

Si no usa recursos existentes o no los crea a través de Azure Portal, este script crea los recursos de Azure necesarios para esta práctica de laboratorio. Le brinda la flexibilidad de crear algunos o todos los recursos necesarios para este laboratorio. Puede ejecutar el script tal cual o modificarlo para adaptarlo a sus necesidades. Los recursos creados por el script incluyen:

* Grupo de recursos
* Cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual

El script tiene un amplio conjunto de parámetros para ayudarlo a personalizar los recursos que se crearán. También utiliza un archivo .env para recuperar y almacenar las variables de entorno necesarias tanto para el script de PowerShell como para las API de la aplicación de búsqueda vectorial.

" Si bien estos parámetros se pueden pasar directamente al script, le recomendamos que utilice el archivo .env para completar previamente la información de sus recursos en lugar de agregar los parámetros al ejecutar el script. Esto le facilitará la administración de las variables de entorno. "

Para obtener más información sobre el script de PowerShell y sus parámetros, revise la documentación create-azure-resources.ps1.

" Asegúrese de que el inquilino, la ubicación y la suscripción que utiliza permitan la creación de los recursos necesarios. Es posible que no todas las ubicaciones y suscripciones permitan o admitan la creación de todos los recursos necesarios para esta práctica de laboratorio. Si tiene algún problema, comuníquese con a su administrador de Azure ".

# Ejecute el script create-azure-resources.ps1 para crear los recursos de Azure necesarios

Para crear los recursos de Azure necesarios para esta práctica de laboratorio:

1. Ejecute el siguiente comando en la terminal integrada.

potencia Shell
inicio de sesión az
./create-azure-resources.ps1

2. Copie y guarde las variables de entorno devueltas por el script en caso de que las necesite más adelante. Puede verificar los recursos creados en Azure Portal.

3. Asegúrese de que el archivo .env contenga la información del recurso.

" La cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual necesitará una regla de firewall para permitir el acceso desde su dirección IP pública actual. Si su cuenta de Azure Cosmos DB fue generada por el script create-azure-resources.ps1, debería haber creado el regla de firewall por usted. Verifique las reglas de firewall existentes en la sección Configuración de red de la cuenta de Azure Cosmos DB. Si no está seguro de cuál es su dirección IP pública actual, puede usar el siguiente comando para averiguarlo: "
potencia Shell
Invocar-RestMethod -Uri 'http://ipinfo.io/ip' -Method Obtener
Una vez que se crean los recursos y su archivo .env se completa con la información del recurso, puede continuar con el siguiente paso.

# Instale y cargue datos en la edición comunitaria de MongoDB en su máquina local
A menos que tenga instalado un servidor MongoDB que no sea de producción con acceso a Internet, instalemos la edición comunitaria de MongoDB en su máquina local. Para obtener más información sobre cómo realizar esta instalación, revise las instrucciones en la documentación oficial de MongoDB.

# Instalar la edición comunitaria MongoDB
Instalemos la edición comunitaria de MongoDB en su máquina local.

1. Abra su navegador y vaya a la página de descarga del servidor comunitario MongoDB desde el sitio web oficial de MongoDB.

3. Seleccione el botón Seleccionar paquete y seleccione la configuración adecuada para su entorno. Por ejemplo, si usa Windows, seleccione la plataforma Windows x64 y el paquete msi.

| Versión | 6.0.14 | | Plataforma | Su sistema operativo/plataforma actual | | Paquete | Su tipo de paquete de instalación actual |

3. Seleccione el botón Descargar para descargar el instalador.

4. Una vez descargado el instalador, ejecútelo y siga las instrucciones de instalación para una instalación completa.

* Elija todas las opciones predeterminadas.
* El nombre del servicio debe ser MongoDB.
* Seleccione Instalar MongoDB Compass.

Esta instalación debería tardar unos minutos en completarse.

5. Una vez que se complete la instalación, seleccione el botón Finalizar para cerrar el instalador si es necesario.

# Instalar las herramientas de base de datos MongoDB
Necesitamos algunas herramientas que nos ayuden con el proceso de migración. Instalemos las herramientas de base de datos MongoDB en su máquina local.

1. Abra su navegador y vaya a la página de descarga de herramientas de base de datos de línea de comandos de MongoDB desde el sitio web oficial de MongoDB.

2. Seleccione la configuración adecuada para su entorno. Por ejemplo, si usa Windows, seleccione la plataforma Windows x86_64 y el paquete msi.
| Versión | 100.9.4 o la última versión | | Plataforma | Su sistema operativo/plataforma actual | | Paquete | Su tipo de paquete de instalación actual |

3. Seleccione el botón Descargar para descargar el instalador.

4. Una vez descargado el instalador, ejecútelo y siga las instrucciones de instalación para una instalación completa. Elija todas las opciones predeterminadas.

5. Una vez que se complete la instalación, seleccione el botón Finalizar para cerrar el instalador si es necesario.

# Es hora de verificar la instalación.

1. Cierre Visual Studio Code y vuelva a abrirlo para asegurarse de que las variables de entorno estén cargadas.

2. Haga clic derecho en la carpeta 02-migrate y seleccione Abrir en Terminal integrada.

3. En las ventanas de la terminal, ejecute el siguiente comando para verificar la instalación:
Si el servidor está en funcionamiento, responderá aproximadamente cada segundo; si está inactivo, eventualmente expirará después de aproximadamente un minuto.
Si el servidor no funciona, siga las instrucciones de la documentación oficial de MongoDB para iniciar el servidor.

" Si bien la instalación de MongoDB y sus herramientas debería haber actualizado su variable de entorno PATH, si no se encuentra el comando, especifique la ruta al llamar al comando mongostat. Por ejemplo, si instaló las herramientas en la ubicación predeterminada en el entorno de Windows, puede ejecutar el siguiente comando para verificar la instalación (reemplace la ruta con la ruta real donde se instalaron las herramientas y use esa ruta en los otros comandos de herramientas de MongoDB en esta práctica de laboratorio): "
intento
& "C:\Archivos de programa\MongoDB\Tools\100\bin\mongostat"
Ahora deberíamos tener un servidor MongoDB en ejecución en su máquina local. Carguemos algunos datos en él.

# Cargar datos en la edición comunitaria de MongoDB
1. Abra una nueva terminal y navegue hasta la carpeta de instalación de Herramientas MongoDB.

2. Ejecute el siguiente comando para cargar los datos de muestra en el servidor MongoDB:

" bash
& mongoimport --host localhost --port 27017 --db cosmicworks --collection customers --jsonArray --file ../data/cosmicworks/customers.json
& mongoimport --host localhost --port 27017 --db cosmicworks --collection products --jsonArray --file ../data/cosmicworks/products.json
& mongoimport --host localhost --port 27017 --db cosmicworks --collection salesOrders --jsonArray --file ../data/cosmicworks/salesOrders.json "

Este comando carga los datos de muestra en el servidor MongoDB que se ejecuta en su máquina local.

Ahora deberíamos tener un servidor MongoDB en ejecución con algunos datos; es hora de migrarlo a Azure Cosmos DB basado en núcleo virtual para MongoDB.

# Migrar a una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual mediante herramientas nativas de MongoDB (sin conexión)

Para exportar los datos desde el servidor MongoDB local e importarlos a la cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual, use las herramientas nativas MongoDB mongodump y mongorestore. En un entorno de producción, si su base de datos es grande, es posible que deba buscar otras formas de migrar la base de datos, como a través del Servicio de migración de datos de Azure.

1. Vuelque los datos de su servidor MongoDB local en un archivo BSON. Ejecute el siguiente comando en la terminal:

bash
& mongodump --host localhost --puerto 27017 --db cosmicworks --out ../data/cosmicworks
Este comando crea un archivo BSON en la carpeta ../data/cosmicworks. El comando mongodump genera el progreso de la operación de volcado.

2. Restaure los datos volcados en su servidor Azure Cosmos DB para MongoDB basado en núcleo virtual. Reemplace,, yourMongoDBClusterName y yourDatabaseName con su nombre de usuario, contraseña, nombre del clúster de Azure MongoDB y nombre de la base de datos reales:

bash
& mongorestore --uri "mongodb+srv://<user>:<password>@yourMongoDBClusterName.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000" --db cosmicworks1 ../data/cosmicworks/cosmicworks
This command restores the BSON file into your vCore-based Azure Cosmos DB for MongoDB server. The mongorestore command outputs the progress of the restore operation.

" No olvide asegurarse de que las reglas de firewall para su cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual estén configuradas para permitir el acceso desde su dirección IP pública actual. Si su cuenta de Azure Cosmos DB fue generada por create-azure-resources. ps1, debería haber creado la regla de firewall por usted. Verifique las reglas de firewall existentes en la sección Configuración de red de la cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual. Si no está seguro de cuál es su dirección IP pública actual, puede hacerlo. Utilice el siguiente comando para averiguarlo: "
potencia Shell
Invocar-RestMethod -Uri 'http://ipinfo.io/ip' -Method Obtener

# Verifiquemos que la migración se completó exitosamente.

1. Abra la aplicación MongoDB Compass.
2. Conéctese a su cadena de conexión de Azure Cosmos DB para MongoDB basada en núcleo virtual.
3. Seleccione Continuar en la pantalla de advertencia.
4. Debería ver su base de datos, colecciones y documentos en el panel de navegación izquierdo.
5. Cierre la aplicación MongoDB Compass.

" Tenga en cuenta que, si bien usó las herramientas mongodump y mongorestore para migrar los datos desde su servidor MongoDB local a la cuenta de Azure Cosmos DB para MongoDB basada en vCore, también podríamos haber usado las herramientas mongoexport y mongoimport para hacer lo mismo. "

Ahora debería tener un servidor Azure Cosmos DB para MongoDB basado en núcleo virtual en ejecución con los datos de su servidor MongoDB local. Migró correctamente los datos desde su servidor MongoDB local a la cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual mediante las herramientas nativas de MongoDB.

# Limpiar
Después de completar los ejercicios de laboratorio, es importante limpiar todos los recursos que haya creado para evitar incurrir en costos innecesarios. Así es cómo:

1. Portal de Azure: inicie sesión en el portal de Azure.

2. Eliminar grupo de recursos: si creó un nuevo grupo de recursos para esta práctica de laboratorio, navegue hasta Grupos de recursos, busque su grupo y elimínelo. Esta acción elimina todos los recursos que contiene, incluida la instancia de Azure Cosmos DB y cualquier recurso de Azure OpenAI.

3. Eliminar manualmente recursos individuales: si agregó recursos a un grupo existente, deberá eliminar cada recurso individualmente. Navegue hasta cada recurso creado para este laboratorio (por ejemplo, Azure Cosmos DB para MongoDB, cuenta de Azure OpenAI) y elimínelos.

4. Verifique la eliminación: confirme que todos los recursos que ya no necesita se eliminaron correctamente y ya no aparecen en su Azure Portal.

5. Revise la facturación: consulte la sección de facturación de Azure para asegurarse de que no se produzcan cargos inesperados y verifique que todos los recursos no deseados se hayan eliminado correctamente.

Este proceso de limpieza ayuda a mantener su cuenta de Azure organizada y libre de cargos innecesarios, lo que garantiza que solo pague por los recursos que utiliza activamente.

# Conclusión

Migró correctamente una base de datos MongoDB a una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual mediante las herramientas nativas de MongoDB. Hay varias otras formas de migrar una base de datos MongoDB a una cuenta de Azure Cosmos DB para MongoDB basada en núcleo virtual, incluido el uso de Azure Data Studio para migraciones sin conexión y Azure Databricks para migraciones en línea/sin conexión. El método que elija depende de sus requisitos y limitaciones específicos.

