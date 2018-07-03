## What is the command to clear and flush magento cache
 To clean the cache 
  php bin/magento cache:clean
  To flush cache
  php bin/magento cache:flush

## In which directory we write our own custom module in Magento2
If we need to create our own module e.g Hello World then we define it in
app/code folder. It will be app/code/VendorName/moduleName.
e.g : app/code/Letsknowit/Hello_world.

## What is Magento?
Magento is an ecommerce platform that enables companies to run and manage their ecommerce sites in an optimized way. Magento functions as an open source ecommerce management system. It was first published by a Varien Inc in 2008, before being sold to eBay and ultimately spun off into its own entity. The 2.0 version of Magento arrived in November of 2015 and has improved the platform across the board.

## Which are the methods of PayPal Payment Gateways?
The two methods of PayPal Payment Gateways are:
	Payflow Pro (Includes Express Checkout)
	Payflow Link (Includes Express Checkout)

## Why is Magento valuable for businesses?
Magento is valuable for businesses because it gives them a high level of control and flexibility when they are managing the look, functionality, and content of their ecommerce store. The Magento software is both extremely convenient, and extremely effective for running an ecommerce operation.
Further, it has a number of features that make operating an ecommerce site easier compared to other options. Many of these features revolve around how financial transactions are made, and how content can be uploaded and optimized for search engine rankings.  

## What are disadvantages of Magento?
The disadvantages of Magento are:
	Magento uses larger disk space and memory.
	It takes much time to build the customized functionality.
	It is very slow compared to other E-commerce sites.
	It needs proper hosting environment, if the hosting environment is improper the user can face the problems.

## What are the different versions of Magento?
Magento categorizes their product across multiple offerings:
	Magento Commerce
	Magento Order Management
	Magento Business Intelligence
	Magento Shipping
	Magento Social
	Magento Open Source

## How to enable Maintenance mode in Magento?
To enable Magento Maintenance mode, create  a file named maintenance.flag and upload to your Magento home directory. The file contains the following code:
```
$maintenanceFile = ‘maintenance.flag’;
if (file_exists($maintenanceFile)) {
include_once dirname(__FILE__) . ‘/errors/503.php’;
exit;
}
```

## Name the web-server that supports magento?
The Web-server that supports Magento are:
	Apache 2.x
	Nginx 1.7.x

