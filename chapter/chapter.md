# Azure Data Services

This chapter focuses on an overview of the many data services within the Microsoft Azure cloud. We detail the different relational and non-relational NoSQL databases as well as the many data analytics services.

## Database Products

### Azure SQL Database

#### Overview

The Azure SQL database is the cloud-based, SQL Server database as a service, relational database engine using the latest version of the SQL Server. There are many advantages to using an Azure SQL database as opposed to an on-premises SQL Server database platform. There are also many pricing level choices based on a function of hardware resources used.

#### Advantages

The biggest advantage to using an Azure SQL database rather than an on-premesis SQL database is scalability. Users can choose from many options of pricing model depending upon the utilization of their needs. Companies can start out with a low cost Azure SQL database having a fully managed database platform without the expense of an on-premises server and administrative costs and quickly scale up to a higher-cost pricing model with expanded system resources. Other major benefits are database high availability and low administrative duties with operational database administrator or Windows server administration duties [fa18-516-06-AzureSQL2].

#### Pricing Models

There are two purchasing models. The Database Transaction Unit (DTU) based model and the vCore based model. The DTU model uses a measure using a combination of "compute, memory, and storage" [fa18-516-06-AzureSQL1]. In the DTU purchasing model, users can choose from three different configurations, Basic, Standard, and Premium, corresponding to the extent of the needed resources. Within the vCore model, users can individually choose the compute, memory, and storage values. The Gen4 generation allows for up to 24 virtual CPU cores and 168 GB memory and the Gen5 generation allows for up to 80 virtual cores and 408 GB memory. The maximum data size within the Gen4 is 1 TB and with Gen5 it is 4 TB.

#### Creating an Azure SQL Database

The creation of an Azure SQL database is very easy:

1. Log in to the Azure portal
2. From the Azure portal, select "Create a Resource", then choose "SQL Database" within "Databases"
3. Enter the name of the database to create
4. Enter the container for the resource group, create a new resource group, if desired
5. Choose if this created database will use an elastic pool
6. Select the pricing model
7. Click the "Create" button

![alt text](https://github.com/cloudmesh-community/fa18-516-06/blob/master/chapter/Azure_CreateSQLDatabase.JPG)

Once the database has been created, we can use Microsoft Visual Studio as the development tool to the new Azure SQL database, much like an on-premesis database using SQL Server Management Studio, as shown below.

![alt text](https://github.com/cloudmesh-community/fa18-516-06/blob/master/chapter/Azure_SQLDBConnect.JPG)


### Azure MySQL PostgreSQL, MariaDB Databases

Within the Azure ecosystem, it is possible to use three different open-source databases, MySQL, PostgreSQL, and MariaDB. Each of these are the cloud-based community versions of the databases. Much like Azure SQL, these have the benefits of using a cloud-based database service, for example scalability and uptime. These Azure relational database allow users to keep using their desired open-source database platforms in the Azure cloud environment [fa18-516-06-AzureOpenSourceDB].



### Cosmos DB

    
    
    
## Analytics

### Azure SQL Data Warehouse
        
        
### Azure HDInsight (Kafka)
        
        
        
### Azure Machine Learning


### Azure Stream Analytics



### Azure Data Lake Store
        
        
        
### Azure Data Lake Analytics
        
        
        
### Azure Data Catalog
        
        
        
### Azure Data Factory
        
        
        
### Azure Databricks
        
        
        
### Azure Blob Storage
        
        
        
### Azure Analysis Services
        
        
        
### PowerBI



